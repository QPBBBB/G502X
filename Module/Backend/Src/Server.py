import argparse as Argparse
import errno as Errno
import json as Json
import webbrowser as Webbrowser
from http.server import ThreadingHTTPServer
from Routes.HttpRoutes import HttpRoutes
from Services.DeviceService import DeviceService


def Main():
    Parser = Argparse.ArgumentParser(description='G502 X 本机 DPI 服务')
    Parser.add_argument('--port', type=int, default=8765)
    Parser.add_argument('--probe', action='store_true', help='只读发现设备后退出')
    Parser.add_argument('--open-browser', action='store_true', help='启动后打开控制页面')
    Arguments = Parser.parse_args()
    Service = DeviceService()
    if Arguments.probe:
        print(Json.dumps(Service.Discover(), ensure_ascii=False, indent=2))
        return
    try:
        Server = ThreadingHTTPServer(('127.0.0.1', Arguments.port), HttpRoutes)
    except OSError as Error:
        # 双击入口遇到旧服务占用时，使用空闲端口打开本次独立环境的页面。
        if not Arguments.open_browser or (Error.errno != Errno.EADDRINUSE and getattr(Error, 'winerror', None) != 10013):
            raise
        Server = ThreadingHTTPServer(('127.0.0.1', 0), HttpRoutes)
    Server.Service = Service
    print(f'打开 http://127.0.0.1:{Server.server_port} ，按 Ctrl+C 停止。', flush=True)
    try:
        if Arguments.open_browser:
            Webbrowser.open(f'http://127.0.0.1:{Server.server_port}/')
        Server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        Server.server_close()


if __name__ == '__main__':
    Main()
