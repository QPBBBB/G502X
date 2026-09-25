# HID++ 协议及实机边界

参考只读目录 `D:/Projects/OpenLogi`：

- `crates/openlogi-hidpp/src/feature/adjustable_dpi.rs`：特性 `0x2201`，函数 0 获取传感器数，1 获取 DPI 支持列表，2 读取 DPI，3 设置 DPI。
- `crates/openlogi-hidpp/src/feature/device_type_and_name.rs`：特性 `0x0005` 获取设备名称。
- `crates/openlogi-device-registry/src/receiver.rs`：`0xC547` LIGHTSPEED 接收器的 G502 X 参考验证注释。该注释不等于本项目已验证全部功能。
- `crates/openlogi-hid/src/transport/windows.rs`：短/长 HID 集合按物理接口分组的思路。

USB 厂商为 `0x046D`。向接收器槽位 1–6 发起只读查询；Root 特性 `0x0000` 的函数 0 将特性 ID 转为运行时索引，绝不硬编码 `0x2201` 的索引。发送 20 字节长报告 `0x11`；接收短报告 `0x10` 和长报告 `0x11`。消息包含槽位、特性索引、函数高半字节和非零 SoftwareId 低半字节。Windows 上读取长集合 `FF00:0002` 及对应短集合 `FF00:0001`。错误报告 `0x8F` / `0xFF` 单独匹配；不存在的接收器槽位不算鼠标故障。

DPI 数据为大端，列表首字节为传感器索引；随后每两个字节一个显式值，零终止。`0xE000 | Step` 表示前一个值到后一个值之间的范围，末端即使不整除也保留。展开后排序去重，设置值必须属于实际返回列表；统一差值才显示固定步进。

本次实机只读记录（2026-09-25）：发现一个接收器，名称 `G502 X LIGHTSPEED`，DPI `800`，最小 `100`，最大 `25600`，步进 `50`。也观察到后续只读请求超时；原因未能仅由报告确定，页面按不可达处理。写入功能仅在模拟传输中验证编码、输入拒绝和读回不一致处理，没有对实机执行函数 3。未验证板载持久化，不承诺跨模式或跨固件表现。

Python HID 依赖使用 [cython-hidapi](https://github.com/trezor/cython-hidapi)，固定版本见 requirements.txt。本项目参考代码许可及来源见 ThirdPartyNotices.md。
