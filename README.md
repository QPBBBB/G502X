# G502 X DPI 第一版

精简深色单页：显示鼠标连接状态、当前 DPI、设备支持范围及步进，输入 DPI 后点击“应用”。输入必须符合设备实际支持值。网页通过同源 HTTP 调用 Python 本机后台，后台通过 hidapi 与 LIGHTSPEED 接收器通信。

## 启动（Windows / PowerShell）

需要 Python 3.12 或更高版本。首次在项目根目录执行：

```powershell
cd D:/Projects/G502X
python -m venv .venv
& ./.venv/Scripts/python.exe -m pip install -r module/Backend/requirements.txt
```

本次开发已经创建 `.venv` 并安装依赖，可直接启动：

```powershell
& ./Scripts/Start.ps1
```

打开 http://127.0.0.1:8765 。请使用这个地址，不用 `localhost`，也不要直接双击 HTML。按 Ctrl+C 停止。端口被占用时使用 `& ./Scripts/Start.ps1 -Port 8766`。

如果 PowerShell 脚本执行策略限制运行，可直接执行：

```powershell
& ./.venv/Scripts/python.exe module/Backend/Src/Server.py
```

没有安装可用 Python 时，请先安装 Python；WindowsApps 的 `python.exe` 可能只是应用商店占位程序。项目不依赖 Codex 的运行时路径。

## 验证

```powershell
# 只读探测，不执行设置 DPI：
& ./.venv/Scripts/python.exe module/Backend/Src/Server.py --probe
```

已在本机只读识别到 `G502 X LIGHTSPEED`，当前 DPI 为 `800`，支持 `100–25600`、步进 `50`。后续读取也遇到过不可达超时，页面正确清空当前值并禁用设置；没有将接收器枚举成功视为鼠标连接成功。**真实 DPI 写入、断电保存和所有休眠/重连场景尚未完成实机验证**，本次未改变真实鼠标 DPI。

## 范围和排错

- 第一版仅发现 Logitech `046D:C547` 接收器，并核验设备名称包含 `G502 X`；有线连接、其他接收器型号不在本版范围内。
- 接收器存在但鼠标未响应时，显示“鼠标休眠、关闭或不可达”；请移动鼠标唤醒，确认电源，必要时退出 G HUB 后点“重新检测”。无法仅凭超时区分休眠与无线断连。
- 连接后每 5 秒读取一次状态，页面在后台时暂停轮询；读失败后停止轮询，手动重新检测恢复。
- 多个目标设备同时存在时禁用设置，请仅保留一个目标接收器。
- 仅设置传感器 0 的当前 DPI，不管理板载配置、DPI 档位、按键或持久化。G HUB / 板载模式可能覆盖当前值。
- 写入后读回确认；不自动重试写入。写入超时或读回失败时，设备可能已经接受设置，应重新检测确认。
- 仅监听 `127.0.0.1`。检查 Host、Origin 和 Fetch Metadata，写请求只接受本机同源 JSON；这不是对恶意本机进程的隔离机制。

目录职责见 [Docs/Architecture.md](Docs/Architecture.md)，协议与许可见 [Docs/ProtocolNotes.md](Docs/ProtocolNotes.md)，接口见 [module/Api/OpenApi.yaml](module/Api/OpenApi.yaml)。
