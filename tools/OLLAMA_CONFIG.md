# Ollama 搜索集成配置说明

## 当前配置

- **本地 API 地址**：`http://127.0.0.1:443/api/generate`
- **公网 API 地址**：`http://frp-bar.com:56559/api/generate`
- **模型**：`deepseek`（可根据你的部署调整）

## 需要做的准备工作

### 1. 确认 Ollama 模型已加载

在你的 Ollama 服务器上运行：

```bash
ollama list
```

确保 `deepseek` 或你要使用的模型已经加载。如果没有，运行：

```bash
ollama pull deepseek
```

或其他模型（如 `llama2`、`mistral` 等）：

```bash
ollama pull llama2
```

### 2. 验证 API 连接

在本地或公网上测试 API：

```bash
# 本地测试
curl -X POST http://127.0.0.1:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek",
    "prompt": "Hello",
    "stream": false
  }'

# 公网测试
curl -X POST https://frp-bar.com:56559/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek",
    "prompt": "Hello",
    "stream": false
  }'
```

如果收到响应，说明 API 正常工作。

### 3. 启动 Ollama 服务

**推荐方式：使用提供的启动脚本**

Windows 用户可以直接运行：

```bash
# 双击运行
tools\start_ollama.bat
```

或在 PowerShell 中：

```powershell
# 右键运行
tools\start_ollama.ps1
```

这些脚本会自动设置正确的环境变量并启动服务。

**手动启动方式：**

```bash
# 设置环境变量指定端口
$env:OLLAMA_HOST = "127.0.0.1:443"
$env:OLLAMA_ORIGINS = "*"

# 启动服务
ollama serve
```

或者在 PowerShell 中：

```powershell
$env:OLLAMA_HOST = "127.0.0.1:443"
$env:OLLAMA_ORIGINS = "*"
ollama serve
```

**重要：** 确保 Ollama 确实在443端口监听。你可以用以下命令检查：

```bash
netstat -ano | findstr :443
```

如果没有看到 Ollama 进程，说明启动失败。

### 4. 如果使用不同的模型名称

编辑 `source/js/deepseek-search.js`，找到这一行：

```javascript
model: 'deepseek',  // 请根据你的 Ollama 模型名称修改
```

改为你的模型名称，例如：

```javascript
model: 'llama2',  // 或其他你部署的模型
```

### 4. CORS 配置

如果遇到 CORS 错误，需要在 Ollama 启动时配置允许跨域请求。

在启动 Ollama 时设置环境变量：

```bash
# Windows (PowerShell)
$env:OLLAMA_ORIGINS = "*"
ollama serve

# Linux/Mac
export OLLAMA_ORIGINS="*"
ollama serve
```

或在 `~/.ollama/config.json` 中配置：

```json
{
  "allow_origins": ["*"]
}
```

## 当前搜索工作原理

搜索脚本使用你的 Ollama 模型来：

1. 理解用户的查询意图
2. 生成相关的关键词和主题
3. 返回模型的响应

这不是真正的向量搜索，而是基于文本生成的智能响应。

## 改进建议

如果需要真正的向量搜索，可以考虑：

1. **使用 Ollama 的嵌入模型**：
   ```bash
   ollama pull nomic-embed-text
   ```

2. **构建本地向量索引**：使用 Python 脚本预处理文档，生成向量，存储在本地

3. **使用混合搜索**：结合关键词搜索和向量相似度搜索

## 故障排除

### "模型不存在"错误

确保模型已加载：
```bash
ollama pull deepseek
ollama list
```

### CORS 错误

检查 Ollama 是否允许跨域请求，按上面的方法配置。

### 连接超时

- 检查 Ollama 是否在443端口运行：
  ```bash
  netstat -ano | findstr :443
  ```
- 检查 FRP 映射是否正常工作
- 在浏览器中测试：`http://127.0.0.1:443/`
- 检查防火墙设置

### 公网连接失败

公网连接需要：
1. FRP 服务正确映射端口
2. Ollama 监听在正确的端口
3. 网络连接正常

### API 响应为空

- 检查模型是否正确加载
- 尝试在终端直接测试 API
- 检查模型的参数和提示词格式

### 快速诊断步骤

1. **检查 Ollama 状态**：
   ```bash
   ollama list
   ollama ps
   ```

2. **检查端口监听**：
   ```bash
   netstat -ano | findstr :443
   ```

3. **测试本地连接**：
   ```bash
   curl http://127.0.0.1:443/api/tags
   ```

4. **测试公网连接**：
   ```bash
   curl https://frp-bar.com:56559/api/tags
   ```

5. **如果都失败，重新启动 Ollama**：
   ```bash
   # 停止现有服务
   taskkill /f /im ollama.exe 2>nul
   
   # 设置环境变量
   $env:OLLAMA_HOST = "127.0.0.1:443"
   $env:OLLAMA_ORIGINS = "*"
   
   # 启动服务
   ollama serve
   ```
