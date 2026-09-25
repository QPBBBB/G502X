# 架构与命名

```text
module/
  Frontend/
    index.html
    Src/
      Pages/DpiPage.js
      Api/DeviceApi.js
      Style.css
  Backend/
    requirements.txt
    Src/
      Server.py
      Routes/HttpRoutes.py
      Services/DeviceService.py
      Device/Transport/HidTransport.py
      Device/Hidpp/Protocol.py
  Api/OpenApi.yaml
Docs/
  Architecture.md
  ProtocolNotes.md
  ThirdPartyNotices.md
Scripts/
  Start.ps1
README.md
```

前端为原生 HTML/CSS/JavaScript，无构建步骤。只有一个深色页面，不为预览中的 Components 目录制造空组件。DeviceApi 统一 JSON 请求；DpiPage 处理发现、显示、轮询、数字输入校验和用户触发的应用。

Server 固定回环监听，HttpRoutes 提供静态资源白名单、HTTP 输入校验和错误映射。DeviceService 用锁串行处理设备访问，每次发现重新构建不透明设备 Id 映射，不接受客户端提供 HID 路径或任意原始报告。设置前重新核验名称与支持列表。

HidTransport 管理 hidapi 句柄，并在 Windows 按物理接口配对短报告集合和长报告集合。Protocol 匹配设备槽位、特性索引、函数和 SoftwareId，忽略无关通知，解析范围并验证写后读回。错误不会伪造 DPI 或连接状态。

自定义变量、函数、类型及文件主体使用 PascalCase。标准库回调 `do_GET`、`setup`、第三方 API、`index.html`、`requirements.txt`、`README.md` 等遵循工具约定。注释为中文。项目路径字符串和示例使用 `/`，HID 原生设备路径作为不透明字节串在系统边界原样保留。
