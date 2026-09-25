import hashlib as Hashlib
import threading as Threading
from Device.Hidpp.Protocol import DeviceError, Protocol
from Device.Transport.HidTransport import Enumerate, HidTransport


class DeviceService:
    def __init__(Self):
        Self.Lock = Threading.Lock()
        Self.Targets = {}

    def Discover(Self):
        with Self.Lock:
            Self.Targets = {}
            Devices, Errors = [], []
            Receivers = Enumerate()
            for Receiver in Receivers:
                Transport = None
                try:
                    Transport = HidTransport(Receiver['path'])
                    for Slot in range(1, 7):
                        try:
                            Client = Protocol(Transport, Slot)
                            Name = Client.Name()
                            if 'G502 X' not in Name.upper():
                                continue
                            State = Client.ReadDpi()
                            Id = Hashlib.sha256(Receiver['path'] + bytes([Slot])).hexdigest()[:20]
                            Self.Targets[Id] = (Receiver['path'], Slot)
                            Devices.append({'Id': Id, 'Name': Name, 'Connected': True, **State})
                        except DeviceError as Error:
                            if Error.Code not in ('Timeout', 'Unavailable'):
                                Errors.append({'Code': Error.Code, 'Message': f'槽位 {Slot}: {Error}'})
                except OSError:
                    Errors.append({'Code': 'TransportError', 'Message': '无法打开接收器，请检查连接或退出占用设备的软件。'})
                finally:
                    if Transport:
                        Transport.Close()
            return {'ReceiverCount': len(Receivers), 'Devices': Devices, 'Errors': Errors}

    def Access(Self, Id, Dpi=None):
        with Self.Lock:
            if Id not in Self.Targets:
                raise DeviceError('NotFound', '设备已失效，请重新发现设备。')
            Path, Slot = Self.Targets[Id]
            Transport = None
            try:
                Transport = HidTransport(Path)
                Client = Protocol(Transport, Slot)
                Name = Client.Name()
                if 'G502 X' not in Name.upper():
                    raise DeviceError('NotFound', '接收器槽位中的设备已变化，请重新发现。')
                State = Client.ReadDpi() if Dpi is None else Client.SetDpi(Dpi)
                return {'Id': Id, 'Name': Name, 'Connected': True, **State}
            except OSError as Error:
                raise DeviceError('Disconnected', '设备连接中断，请重新发现设备。') from Error
            finally:
                if Transport:
                    Transport.Close()
