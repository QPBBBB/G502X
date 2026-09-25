# 第三方参考

DPI 列表解析与 HID++ 调用语义参考 OpenLogi 的 openlogi-hidpp（0BSD）：

BSD Zero Clause License

Copyright (c) 2025 Lukas Schulte Pelkum

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

接收器标识和 Windows 集合分组的实现思路参考同一 OpenLogi 工程（MIT / Apache-2.0），本项目以 Python 独立实现，没有复制其 Rust 源文件。原工程未修改。

hidapi Python 包按其上游提供的许可证分发，见 https://github.com/trezor/cython-hidapi 。项目在 `Python39/` 中附带 Windows x64 运行环境与依赖：Python 3.9.11、hidapi 0.14.0.post4、setuptools 82.0.1。Python 许可保留于 `Python39/LICENSE.txt`，依赖的许可与元数据保留于 `Python39/Lib/site-packages/` 中各自的 `.dist-info` 目录。
