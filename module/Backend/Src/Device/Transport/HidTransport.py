from Device.Hidpp.Protocol import DeviceError
import sys as Sys
import time as Time


def CollectionKey(Path):
    # 原生 HID 路径是设备标识，边界处保持系统提供的字节串。
    Parts = Path.lower().split(b'#')
    if len(Parts) < 3:
        return Path.lower()
    Hardware = b'&'.join(Part for Part in Parts[1].split(b'&') if not Part.startswith(b'col'))
    Instance = Parts[2].rsplit(b'&', 1)[0]
    return Hardware + b'#' + Instance


def LoadHid():
    try:
        import hid as Hid
        return Hid
    except ImportError as Error:
        raise DeviceError('DependencyMissing', '缺少 hidapi，请安装 Backend/requirements.txt。') from Error


def Enumerate():
    # 第一版限定已知 G502 X 接收器；不把其他罗技设备当成目标鼠标。
    return [Item for Item in LoadHid().enumerate(0x046D, 0xC547)
            if (Item.get('usage_page'), Item.get('usage')) == (0xFF00, 0x0002)]


class HidTransport:
    def __init__(Self, Path):
        Self.Handle = LoadHid().device()
        Self.ShortHandle = None
        try:
            Self.Handle.open_path(Path)
            # Windows 把短、长报告放在不同集合；只配对同一物理接口。
            if Sys.platform == 'win32':
                for Item in LoadHid().enumerate(0x046D, 0xC547):
                    if (Item.get('usage_page'), Item.get('usage')) == (0xFF00, 1) and CollectionKey(Item['path']) == CollectionKey(Path):
                        Self.ShortHandle = LoadHid().device()
                        Self.ShortHandle.open_path(Item['path'])
                        break
        except Exception:
            Self.Close()
            raise

    def Write(Self, Report):
        if Self.Handle.write(Report) != len(Report):
            raise DeviceError('TransportError', 'HID 请求未完整发送。')

    def Read(Self, Timeout):
        Deadline = Time.monotonic() + Timeout / 1000
        while Time.monotonic() < Deadline:
            for Handle in (Self.Handle, Self.ShortHandle):
                if Handle:
                    Report = Handle.read(64, 10)
                    if Report:
                        return Report
        return []

    def Close(Self):
        Self.Handle.close()
        if Self.ShortHandle:
            Self.ShortHandle.close()
