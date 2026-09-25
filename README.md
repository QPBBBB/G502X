# G502 X DPI

为自己的 Logitech G502 X LIGHTSPEED 开发的个人工具，基于 [OpenLogi](https://github.com/AprilNEA/OpenLogi) 的 HID++ 协议实现参考编写。使用 Python 独立实现，运行时无需安装 OpenLogi。

## v0.01

- 深色 Web UI，直接输入 DPI。
- 设备发现、连接状态、当前 DPI、设备支持的范围与步进。
- DPI 输入校验、应用、读回确认和错误提示。
- Python Backend 使用 `hidapi`，仅监听本机，并校验写入请求来源。

当前支持 `046D:C547` 接收器，通过设备名称识别鼠标。尚未实现改键、宏和板载配置保存。

## Roadmap

### v0.01 — DPI Control

当前开发版本：实现 DPI 调节、连接状态与基础 Web UI。

### v0.02 — Button Remapping

计划：实现鼠标改键。

### v0.03 — Mouse Macros

计划：实现鼠标宏。

### v0.04 — Lua Scripting

计划：支持使用 Lua 脚本编写和执行鼠标宏。

### v0.05 — Frontend Improvements

计划：优化前端界面与交互。

### v1.0 — Stable Release

计划：完成正式测试与发布。

## Quick Start

需要 Windows 和 Python 3.12+，在项目根目录执行。

1. 首次创建环境并安装依赖：

```powershell
python -m venv .venv
& ./.venv/Scripts/python.exe -m pip install -r module/Backend/requirements.txt
```

2. 启动本机服务：

```powershell
& ./.venv/Scripts/python.exe module/Backend/Src/Server.py
```

3. 打开 [DPI 页面](http://127.0.0.1:8765)，确认已连接后输入 DPI，点击“应用”。请使用该地址，不要改为 `localhost`。

按 Ctrl+C 停止服务。启动时追加 `--port 8766` 可更换端口；使用 `--probe` 可只读探测设备后退出。鼠标不可达时，先唤醒再重新检测；发生访问冲突时尝试退出 G HUB。

## Agent Guide

- `module/Frontend/`：HTML、CSS、JavaScript，无需构建。
- `module/Backend/Src/`：HTTP Routes、Device Service、HID Transport、HID++ Protocol。
- `module/Api/OpenApi.yaml`：API Contract。
- `Docs/`：架构、协议说明和第三方许可。
- `Scripts/Start.ps1`：可选启动脚本。
- 自定义代码名称使用 PascalCase；英文标题使用 Title Case；路径使用 `/`。标准库、工具要求的名称及命令保持原样，代码注释使用中文。
- 所有开发在当前任务中完成，不唤起其他任务，不遗留测试代码。未经用户指定设置值，不修改真实设备设置。

## Hardware Status

已只读识别 G502 X LIGHTSPEED：800 DPI，范围 100–25600，步进 50。也观察到间歇性不可达。真实设备写入与断电保存尚未验证；当前版本仅修改当前 DPI，G HUB 或板载配置可能覆盖它。

## Credits

感谢 [OpenLogi](https://github.com/AprilNEA/OpenLogi) 提供协议实现参考。许可与来源见 [Third-Party Notices](Docs/ThirdPartyNotices.md)，实现细节见 [Protocol Notes](Docs/ProtocolNotes.md)。
