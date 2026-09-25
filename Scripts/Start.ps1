param([int]$Port = 8765)
$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PythonPath = "$ProjectRoot/Python39/python.exe"
if (-not (Test-Path -LiteralPath $PythonPath)) {
    throw '缺少内置 Python39，请恢复完整项目目录。'
}
& $PythonPath "$ProjectRoot/Module/Backend/Src/Server.py" --port $Port
