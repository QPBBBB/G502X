param([int]$Port = 8765)
$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PythonPath = "$ProjectRoot/.venv/Scripts/python.exe"
if (-not (Test-Path -LiteralPath $PythonPath)) {
    throw '请先按 README.md 创建 .venv 并安装依赖。'
}
& $PythonPath "$ProjectRoot/Module/Backend/Src/Server.py" --port $Port
