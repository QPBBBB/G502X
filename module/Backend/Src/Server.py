import argparse as Argparse
import json as Json
from http.server import ThreadingHTTPServer
from Routes.HttpRoutes import HttpRoutes
from Services.DeviceService import DeviceService


def Main():
    Parser = Argparse.ArgumentParser(description='G502 X 本机 DPI 服务')
    Parser.add_argument('--port', type=int, default=8765)
    Parser.add_argument('--probe', action='store_true', help='只读发现设备后退出')
    Arguments = Parser.parse_args()
    Service = DeviceService()
    if Arguments.probe:
        print(Json.dumps(Service.Discover(), ensure_ascii=False, indent=2))
        return
    Server = ThreadingHTTPServer(('127.0.0.1', Arguments.port), HttpRoutes)
    Server.Service = Service
    print(f'打开 http://127.0.0.1:{Server.server_port} ，按 Ctrl+C 停止。', flush=True)
    try:
        Server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        Server.server_close()


if __name__ == '__main__':
    Main()
