import json as Json
import traceback as Traceback
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit as UrlSplit
from Device.Hidpp.Protocol import DeviceError


Frontend = Path(__file__).resolve().parents[3] / 'Frontend'
Assets = {'/': ('index.html', 'text/html; charset=utf-8'),
          '/Src/Pages/DpiPage.js': ('Src/Pages/DpiPage.js', 'text/javascript; charset=utf-8'),
          '/Src/Api/DeviceApi.js': ('Src/Api/DeviceApi.js', 'text/javascript; charset=utf-8'),
          '/Src/Style.css': ('Src/Style.css', 'text/css; charset=utf-8')}


class HttpRoutes(BaseHTTPRequestHandler):
    # do_GET 等名称是标准库回调，保留原名。
    def setup(Self):
        super().setup()
        Self.connection.settimeout(10)

    def end_headers(Self):
        Self.send_header('Cache-Control', 'no-store')
        Self.send_header('X-Content-Type-Options', 'nosniff')
        Self.send_header('Content-Security-Policy', "default-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
        super().end_headers()

    def Reply(Self, Status, Data):
        Body = Json.dumps(Data, ensure_ascii=False).encode('utf-8')
        Self.send_response(Status)
        Self.send_header('Content-Type', 'application/json; charset=utf-8')
        Self.send_header('Content-Length', str(len(Body)))
        Self.end_headers()
        Self.wfile.write(Body)

    def Error(Self, Status, Code, Message):
        Self.Reply(Status, {'Error': {'Code': Code, 'Message': Message}})

    def Allowed(Self, Write=False):
        Host = f'127.0.0.1:{Self.server.server_port}'
        if Self.headers.get('Host') != Host:
            Self.Error(403, 'ForbiddenHost', '请使用启动时显示的 127.0.0.1 地址。')
            return False
        Origin = Self.headers.get('Origin')
        if (Write and Origin != f'http://{Host}') or (Origin and Origin != f'http://{Host}'):
            Self.Error(403, 'ForbiddenOrigin', '请求来源不允许。请从本机页面操作。')
            return False
        if Self.headers.get('Sec-Fetch-Site') not in (None, 'same-origin', 'none'):
            Self.Error(403, 'ForbiddenOrigin', '禁止跨站请求。')
            return False
        return True

    def Execute(Self, Action):
        try:
            Self.Reply(200, Action())
        except DeviceError as Error:
            Status = {'InvalidDpi': 400, 'NotFound': 404, 'Timeout': 503,
                      'Disconnected': 503, 'DependencyMissing': 503}.get(Error.Code, 502)
            Self.Error(Status, Error.Code, str(Error))
        except OSError:
            Self.Error(503, 'TransportError', 'HID 通信失败，请检查接收器并重试。')
        except Exception:
            Traceback.print_exc()
            Self.Error(500, 'InternalError', '后台发生错误，请查看终端并重启服务。')

    def do_GET(Self):
        if not Self.Allowed():
            return
        Route = UrlSplit(Self.path).path
        if Route in Assets:
            File, ContentType = Assets[Route]
            Body = (Frontend / File).read_bytes()
            Self.send_response(200)
            Self.send_header('Content-Type', ContentType)
            Self.send_header('Content-Length', str(len(Body)))
            Self.end_headers()
            Self.wfile.write(Body)
        elif Route == '/Api/Devices':
            Self.Execute(Self.server.Service.Discover)
        elif Route.startswith('/Api/Devices/') and Route.endswith('/Dpi') and len(Route.split('/')) == 5:
            Self.Execute(lambda: Self.server.Service.Access(Route.split('/')[3]))
        else:
            Self.Error(404, 'NotFound', '接口不存在。')

    def do_POST(Self):
        Self.close_connection = True
        if not Self.Allowed(Write=True):
            return
        Route = UrlSplit(Self.path).path
        if not (Route.startswith('/Api/Devices/') and Route.endswith('/Dpi') and len(Route.split('/')) == 5):
            Self.Error(404, 'NotFound', '接口不存在。')
            return
        if Self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
            Self.Error(415, 'InvalidContentType', '请求必须为 JSON。')
            return
        try:
            Size = int(Self.headers.get('Content-Length', '0'))
            if not 0 < Size <= 1024 or Self.headers.get('Transfer-Encoding'):
                raise ValueError()
            Data = Json.loads(Self.rfile.read(Size))
            if not isinstance(Data, dict) or set(Data) != {'Dpi'} or type(Data['Dpi']) is not int:
                raise ValueError()
        except (ValueError, UnicodeError):
            Self.Error(400, 'InvalidBody', '请求必须仅包含整数 Dpi，且大小不超过 1024 字节。')
            return
        Self.Execute(lambda: Self.server.Service.Access(Route.split('/')[3], Data['Dpi']))
