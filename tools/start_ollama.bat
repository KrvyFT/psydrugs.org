@echo off
REM 设置 UTF-8 编码
chcp 65001 > nul

REM Ollama 启动脚本 - 配置为本地 443 端口

echo Ollama 启动脚本
echo ================

REM 设置环境变量
set OLLAMA_HOST=127.0.0.1:443
set OLLAMA_ORIGINS=*

echo 环境变量已设置：
echo OLLAMA_HOST=%OLLAMA_HOST%
echo OLLAMA_ORIGINS=%OLLAMA_ORIGINS%
echo.

echo 正在启动 Ollama 服务...
echo 如果启动失败，请确保已安装 Ollama 并下载了模型
echo.

REM 启动 Ollama
ollama serve

pause