# Ollama 启动脚本 - PowerShell 版本

# 设置 UTF-8 编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "Ollama 启动脚本" -ForegroundColor Green
Write-Host "================" -ForegroundColor Green

# 设置环境变量
$env:OLLAMA_HOST = "127.0.0.1:11434"
$env:OLLAMA_ORIGINS = "*"

Write-Host "环境变量已设置：" -ForegroundColor Yellow
Write-Host "OLLAMA_HOST=$env:OLLAMA_HOST"
Write-Host "OLLAMA_ORIGINS=$env:OLLAMA_ORIGINS"
Write-Host ""

Write-Host "正在启动 Ollama 服务..." -ForegroundColor Cyan
Write-Host "如果启动失败，请确保已安装 Ollama 并下载了模型" -ForegroundColor Yellow
Write-Host ""

# 启动 Ollama
try {
    ollama serve
} catch {
    Write-Host "启动失败：$_" -ForegroundColor Red
    Write-Host "请检查 Ollama 是否已正确安装" -ForegroundColor Red
    Read-Host "按回车键退出"
}