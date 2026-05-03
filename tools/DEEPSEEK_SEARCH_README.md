# Deepseek AI 搜索集成指南

## 功能说明

本站已集成 **Deepseek AI 语义搜索**功能，允许用户通过自然语言查询在 psydrugs.org 库中进行全文智能搜索。

## 集成文件

- **前端脚本**：`source/js/deepseek-search.js` - 处理搜索 UI 和 API 调用
- **搜索页面**：`source/search/index.md` - 搜索界面
- **配置工具**：`tools/setup_deepseek.py` - 初始化和配置工具

## 快速开始

### 1. 获取 Deepseek API Key

访问 [Deepseek 官网](https://www.deepseek.com/) 注册并申请 API Key。

### 2. 配置 API Key

使用提供的配置工具快速设置：

```bash
python tools/setup_deepseek.py --api-key "YOUR_DEEPSEEK_API_KEY"
```

或者，如果使用自定义 API 地址：

```bash
python tools/setup_deepseek.py --api-key "YOUR_DEEPSEEK_API_KEY" --api-host "https://custom.api.host/v1/search"
```

### 3. 验证集成

生成网站并访问搜索页面：

```bash
hexo clean
hexo generate
hexo server
```

然后在浏览器中打开 `http://localhost:4000/search/`

## 功能特性

- **语义搜索**：不仅支持关键词匹配，还能理解查询意图
- **库限制**：搜索范围限制在 `psydrugs.org` 库内
- **高效检索**：返回相似度最高的 8 条结果
- **用户友好**：支持回车键快速搜索
- **错误处理**：完整的错误提示和日志

## API 响应格式

脚本自动支持以下格式的 API 响应：

```json
{
  "data": [
    {
      "title": "页面标题",
      "path": "/page/path",
      "snippet": "内容摘要",
      "score": 0.95,
      "url": "完整链接"
    }
  ]
}
```

或：

```json
{
  "results": [
    {
      "title": "页面标题",
      "path": "/page/path",
      "snippet": "内容摘要",
      "score": 0.95
    }
  ]
}
```

## 高级配置

### 修改搜索结果数量

编辑 `source/js/deepseek-search.js`，修改：

```javascript
const defaultTopK = 8  // 改为需要的数量
```

### 修改样式

在 `source/js/deepseek-search.js` 中的 `applyDefaultStyles()` 函数内修改 CSS。

或者在搜索页面 `source/search/index.md` 中添加自定义样式。

### 使用自定义 API 端点

在搜索页面中修改 script 标签：

```html
<script 
  src="/js/deepseek-search.js" 
  data-api-key="YOUR_KEY"
  data-api-host="https://your-custom-api.com/search"
></script>
```

## 故障排除

### API Key 未生效

确保在页面中正确设置了 `data-api-key` 属性：

```html
<script src="/js/deepseek-search.js" data-api-key="YOUR_ACTUAL_KEY"></script>
```

### CORS 错误

如果出现跨域错误，请确保：

1. Deepseek API 端点支持 CORS
2. 请求头配置正确
3. API Key 有效且权限充足

### 没有搜索结果

- 检查查询词是否过于具体
- 尝试使用更通用的关键词
- 确保库中确实包含相关内容

## 自定义集成

如需在其他页面集成搜索功能，只需在 HTML 中添加：

```html
<input id="deepseek-query" type="text" placeholder="搜索..." />
<button id="deepseek-search-button">搜索</button>
<div id="deepseek-results"></div>

<script src="/js/deepseek-search.js" data-api-key="YOUR_KEY"></script>
```

脚本会自动初始化搜索框和事件监听器。

## 隐私和安全

- API Key 存储在 HTML 属性中，建议对公共站点进行服务器端代理
- 搜索查询会发送到 Deepseek 服务器
- 考虑使用环境变量或后端代理来保护敏感信息

## 更新日志

**v1.0** (2026-05-03)
- 初始版本
- 集成到主题菜单栏
- 支持自定义 API 配置
