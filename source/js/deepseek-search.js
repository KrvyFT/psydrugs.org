// Deepseek AI 检索前端集成脚本
// 使用方法：
// 1. 在页面 HTML 中添加搜索控件：
//    <input id="deepseek-query" type="text" placeholder="输入问题或关键词" />
//    <button id="deepseek-search-button">搜索</button>
//    <div id="deepseek-results"></div>
// 2. 在页面底部引入此脚本，并通过 data-api-key 传入 Deepseek API Key：
//    <script src="/js/deepseek-search.js" data-api-key="YOUR_DEEPSEEK_API_KEY"></script>
// 3. 如果需要自定义 API 地址，可追加 data-api-host 属性。

;(function () {
  const defaultApiHost = 'http://127.0.0.1:11434/api/generate'
  const publicApiHost = 'https://frp-bar.com:56559/api/generate'
  const defaultRepo = 'psydrugs.org'
  const defaultTopK = 8
  const useOllama = true  // 使用 Ollama 模型

  function getElement(id) {
    return document.getElementById(id)
  }

  function renderResultItem(item) {
    const container = document.createElement('div')
    container.className = 'deepseek-result-item'

    const title = document.createElement('div')
    title.className = 'deepseek-result-title'
    title.textContent = item.title || item.path || '未命名结果'
    container.appendChild(title)

    if (item.path) {
      const link = document.createElement('a')
      link.href = item.path
      link.textContent = item.path
      link.className = 'deepseek-result-path'
      link.target = '_blank'
      container.appendChild(link)
    }

    if (item.snippet) {
      const snippet = document.createElement('p')
      snippet.className = 'deepseek-result-snippet'
      snippet.textContent = item.snippet
      container.appendChild(snippet)
    }

    if (item.score !== undefined) {
      const score = document.createElement('span')
      score.className = 'deepseek-result-score'
      score.textContent = `相似度：${Number(item.score).toFixed(3)}`
      container.appendChild(score)
    }

    return container
  }

  function renderResults(results) {
    const resultBox = getElement('deepseek-results')
    const res = await queryOllama(searchText);  function renderResults(results) {
    const resultBox = getElement('deepseek-results')
    if (!resultBox) return

    resultBox.textContent = ''

    if (!Array.isArray(results) || results.length === 0) {
      resultBox.textContent = '未找到匹配结果，请尝试更改查询词。'
      return
    }

    const list = document.createElement('div')
    list.className = 'deepseek-results-list'

    results.forEach((item) => {
      list.appendChild(renderResultItem(item))
    })

    resultBox.appendChild(list)
  }  async function onSearch() {
    const queryInput = getElement('deepseek-query')
    if (!queryInput) return

    const searchText = queryInput.value.trim()
    if (!searchText) {
      showStatus('请输入搜索关键字或问题后再查询。', true)
      return
    }

    showStatus('正在查询本地模型，请稍候...', false)
    renderResults([])

    try {
      const reply = useOllama ? await queryOllama(searchText) : await queryDeepseek(searchText)
      const results = []

      if (useOllama && reply.response) {
        // Ollama 返回直接响应
        results.push({
          title: 'Ollama 分析结果',
          snippet: reply.response
        })
      } else if (Array.isArray(reply.data)) {
        reply.data.forEach((item) => {
          results.push({
            title: item.title || item.file_name || item.path || '',
            path: item.url || item.path || item.file_path || '',
            snippet: item.snippet || item.text || item.summary || '',
            score: item.score || item.similarity || item.rank || '',
          })
        })
      } else if (Array.isArray(reply.results)) {
        reply.results.forEach((item) => {
          results.push({
            title: item.title || item.path || '',
            path: item.url || item.path || '',
            snippet: item.snippet || item.summary || item.text || '',
            score: item.score || item.similarity || item.rank || '',
          })
        })
      }

      renderResults(results)
      showStatus(`已返回 ${results.length} 条结果。`, false)
    } catch (error) {
      console.error(error)
      showStatus(error.message || '查询失败，请检查 API 连接和配置。', true)
    }
  }
    const formattedResults = [
  {
    title: 'Ollama 分析结果',
    snippet: res.response
  }
];

renderResults(formattedResults);

    resultBox.innerHTML = ''

    if (!Array.isArray(results) || results.length === 0) {
      resultBox.textContent = '未找到匹配结果，请尝试更改查询词。'
      return
    }

    const list = document.createElement('div')
    list.className = 'deepseek-results-list'

    results.forEach((item) => {
      list.appendChild(renderResultItem(item))
    })

    resultBox.appendChild(list)
  }

  function showStatus(message, isError = false) {
    const statusEl = getElement('deepseek-status')
    if (!statusEl) return
    statusEl.textContent = message
    statusEl.style.color = isError ? '#c62828' : '#2e7d32'
  }

  function getApiKey() {
    const script = document.currentScript || document.querySelector('script[src$="deepseek-search.js"]')
    if (!script) return ''
    return script.dataset.apiKey || ''
  }

  function getApiHost() {
    const script = document.currentScript || document.querySelector('script[src$="deepseek-search.js"]')
    if (!script) return defaultApiHost

    // 如果明确指定了 API host，使用指定的
    if (script.dataset.apiHost) {
      return script.dataset.apiHost
    }

    // 否则根据当前页面协议自动选择
    if (window.location.protocol === 'https:') {
      return publicApiHost
    } else {
      return defaultApiHost
    }
  }

  async function queryOllama(query) {
    const body = {
      model: 'deepseek-r1:1.5b',  // 请根据你的 Ollama 模型名称修改
      prompt: `以下是一个文档搜索查询。请基于这个查询找出相关的文档关键词和主题。\n\n查询：${query}\n\n相关关键词：`,
      stream: false,
    }

    const response = await fetch(getApiHost(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      mode: 'cors',
    })

    if (!response.ok) {
      const text = await response.text()
      throw new Error(`Ollama 请求失败：${response.status} ${response.statusText} ${text}`)
    }

    return response.json()
  }

  async function queryDeepseek(query) {
    const apiKey = getApiKey()
    if (!apiKey) {
      throw new Error('Deepseek API key 未设置，请在 script 标签中添加 data-api-key="YOUR_KEY"')
    }

    const body = {
      query: query,
      repository: defaultRepo,
      top_k: defaultTopK,
      filter: {
        repo: defaultRepo,
      },
      client: 'static-frontend',
      source: 'psydrugs.org',
    }

    const response = await fetch(getApiHost(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify(body),
      mode: 'cors',
    })

    if (!response.ok) {
      const text = await response.text()
      throw new Error(`Deepseek 请求失败：${response.status} ${response.statusText} ${text}`)
    }

    return response.json()
  }

  async function onSearch() {
    const queryInput = getElement('deepseek-query')
    if (!queryInput) return

    const searchText = queryInput.value.trim()
    if (!searchText) {
      showStatus('请输入搜索关键字或问题后再查询。', true)
      return
    }

    showStatus('正在查询本地模型，请稍候...', false)
    renderResults([])

    try {
      const reply = useOllama ? await queryOllama(searchText) : await queryDeepseek(searchText)
      const results = []

      if (Array.isArray(reply.data)) {
        reply.data.forEach((item) => {
          results.push({
            title: item.title || item.file_name || item.path || '',
            path: item.url || item.path || item.file_path || '',
            snippet: item.snippet || item.text || item.summary || '',
            score: item.score || item.similarity || item.rank || '',
          })
        })
      } else if (Array.isArray(reply.results)) {
        reply.results.forEach((item) => {
          results.push({
            title: item.title || item.path || '',
            path: item.url || item.path || '',
            snippet: item.snippet || item.summary || item.text || '',
            score: item.score || item.similarity || item.rank || '',
          })
        })
      }

      renderResults(results)
      showStatus(`已返回 ${results.length} 条结果。`, false)
    } catch (error) {
      console.error(error)
      showStatus(error.message || '查询失败，请检查 API 连接和配置。', true)
    }
  }

  function attachSearchListeners() {
    const button = getElement('deepseek-search-button')
    const queryInput = getElement('deepseek-query')
    if (!button || !queryInput) return

    button.addEventListener('click', onSearch)
    queryInput.addEventListener('keydown', function (event) {
      if (event.key === 'Enter') {
        event.preventDefault()
        onSearch()
      }
    })
  }

  function applyDefaultStyles() {
    const style = document.createElement('style')
    style.textContent = `
      .deepseek-results-list { margin: 0; padding: 0; }
      .deepseek-result-item { padding: 14px 16px; border-bottom: 1px solid #e0e0e0; }
      .deepseek-result-title { font-weight: 700; margin-bottom: 6px; }
      .deepseek-result-path { display: block; color: #1e88e5; margin-bottom: 8px; text-decoration: none; }
      .deepseek-result-path:hover { text-decoration: underline; }
      .deepseek-result-snippet { margin: 0; color: #424242; }
      .deepseek-result-score { display: inline-block; margin-top: 8px; font-size: 12px; color: #616161; }
      #deepseek-status { margin-top: 10px; font-size: 14px; }
    `
    document.head.appendChild(style)
  }

  function init() {
    attachSearchListeners()
    applyDefaultStyles()
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init)
  } else {
    init()
  }
})()
