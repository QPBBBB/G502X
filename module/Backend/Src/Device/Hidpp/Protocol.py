import time as Time


class DeviceError(Exception):
    def __init__(Self, Code, Message):
        super().__init__(Message)
        Self.Code = Code


def ParseDpiList(Payload):
    Values = []
    Offset = 0
    while Offset + 1 < len(Payload):
        Value = int.from_bytes(Payload[Offset:Offset + 2], 'big')
        Offset += 2
        if Value == 0:
            break
        if Value & 0xE000 == 0xE000:
            Step = Value & 0x1FFF
            if not Values or not Step or Offset + 1 >= len(Payload):
                raise DeviceError('InvalidResponse', '设备返回的 DPI 范围无效。')
            End = int.from_bytes(Payload[Offset:Offset + 2], 'big')
            Offset += 2
            if End < Values[-1] or End >= 0xE000:
                raise DeviceError('InvalidResponse', '设备返回的 DPI 范围端点无效。')
            Values.extend(range(Values[-1] + Step, End, Step))
            Values.append(End)
        else:
            Values.append(Value)
    if not Values:
        raise DeviceError('InvalidResponse', '设备没有返回支持的 DPI。')
    return sorted(set(Values))


class Protocol:
    def __init__(Self, Transport, Slot):
        Self.Transport = Transport
        Self.Slot = Slot
        Self.SoftwareId = 0

    def Call(Self, Feature, Function, Parameters=b''):
        # 每个请求更换 SoftwareId；忽略通知、其他设备及不匹配的应答。
        Self.SoftwareId = Self.SoftwareId % 15 + 1
        Command = Function << 4 | Self.SoftwareId
        Report = bytes([0x11, Self.Slot, Feature, Command]) + Parameters.ljust(16, b'\x00')
        Self.Transport.Write(Report)
        Deadline = Time.monotonic() + 0.7
        while Time.monotonic() < Deadline:
            Reply = bytes(Self.Transport.Read(100))
            if len(Reply) < 7 or Reply[0] not in (0x10, 0x11) or Reply[1] != Self.Slot:
                continue
            if Reply[2] in (0x8F, 0xFF) and Reply[3:5] == bytes([Feature, Command]):
                if Reply[2] == 0x8F and Reply[5] in (8, 9):
                    raise DeviceError('Unavailable', '接收器槽位没有可达设备。')
                raise DeviceError('ProtocolError', f'HID++ 错误 0x{Reply[5]:02X}，请唤醒鼠标或关闭占用设备的软件后重试。')
            if Reply[2:4] == bytes([Feature, Command]):
                Expected = 20 if Reply[0] == 0x11 else 7
                if len(Reply) < Expected:
                    raise DeviceError('InvalidResponse', 'HID++ 应答长度不足。')
                return Reply[4:Expected]
        raise DeviceError('Timeout', '设备未响应：请检查接收器、唤醒鼠标，并尝试退出 G HUB。')

    def Feature(Self, Id):
        Index = Self.Call(0, 0, Id.to_bytes(2, 'big'))[0]
        if not Index:
            raise DeviceError('Unsupported', f'设备不支持 HID++ 功能 0x{Id:04X}。')
        return Index

    def Name(Self):
        Index = Self.Feature(0x0005)
        Count = Self.Call(Index, 0)[0]
        Name = b''
        while len(Name) < Count:
            Name += Self.Call(Index, 1, bytes([len(Name)]))
        return Name[:Count].decode('utf-8', errors='replace')

    def ReadDpi(Self):
        Index = Self.Feature(0x2201)
        if Self.Call(Index, 0)[0] < 1:
            raise DeviceError('Unsupported', '设备没有可用传感器。')
        Payload = Self.Call(Index, 1, b'\x00')
        if len(Payload) != 16 or Payload[0] != 0:
            raise DeviceError('InvalidResponse', 'DPI 列表应答无效。')
        Values = ParseDpiList(Payload[1:])
        Current = Self.Call(Index, 2, b'\x00')
        if Current[0] != 0:
            raise DeviceError('InvalidResponse', 'DPI 传感器应答不匹配。')
        Steps = {Right - Left for Left, Right in zip(Values, Values[1:])}
        return {'CurrentDpi': int.from_bytes(Current[1:3], 'big'), 'SupportedDpi': Values,
                'MinDpi': Values[0], 'MaxDpi': Values[-1],
                'DpiStep': next(iter(Steps)) if len(Steps) == 1 else None}

    def SetDpi(Self, Dpi):
        State = Self.ReadDpi()
        if type(Dpi) is not int or Dpi not in State['SupportedDpi']:
            raise DeviceError('InvalidDpi', '请选择设备支持列表中的整数 DPI。')
        Self.Call(Self.Feature(0x2201), 3, b'\x00' + Dpi.to_bytes(2, 'big'))
        # 写入不自动重试；成功必须经过读回确认。
        State = Self.ReadDpi()
        if State['CurrentDpi'] != Dpi:
            raise DeviceError('VerificationFailed', '设备读回值与请求不同，可能被 G HUB 或板载配置覆盖。请刷新确认。')
        return State
