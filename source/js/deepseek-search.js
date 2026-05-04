// DeepSeek AI 搜索前端脚本
// 通过 data-* 参数配置：
// <script
//   src="/js/deepseek-search.js"
//   data-api-key="YOUR_DEEPSEEK_API_KEY"
//   data-api-host="https://api.deepseek.com/v1/chat/completions"
//   data-model="deepseek-chat"
// ></script>

(function () {
  const defaultApiHost = "https://api.deepseek.com/chat/completions";
  const defaultModel = "deepseek-v4-pro";

  function getElement(id) {
    return document.getElementById(id);
  }

  function getScriptTag() {
    return (
      document.currentScript ||
      document.querySelector('script[src$="deepseek-search.js"]')
    );
  }

  function getApiKey() {
    const script = getScriptTag();
    if (!script) return "";
    return (script.dataset.apiKey || "").trim();
  }

  function getApiHost() {
    const script = getScriptTag();
    if (!script) return defaultApiHost;
    return (script.dataset.apiHost || defaultApiHost).trim();
  }

  function getModel() {
    const script = getScriptTag();
    if (!script) return defaultModel;
    return (script.dataset.model || defaultModel).trim();
  }

  function renderResult(answerText) {
    const resultBox = getElement("deepseek-results");
    if (!resultBox) return;

    resultBox.innerHTML = "";

    if (!answerText) {
      resultBox.textContent = "未获取到有效回答，请稍后重试。";
      return;
    }

    const list = document.createElement("div");
    list.className = "deepseek-results-list";

    const item = document.createElement("div");
    item.className = "deepseek-result-item";

    const title = document.createElement("div");
    title.className = "deepseek-result-title";
    title.textContent = "DeepSeek 回答";

    const snippet = document.createElement("p");
    snippet.className = "deepseek-result-snippet";
    snippet.textContent = answerText;

    item.appendChild(title);
    item.appendChild(snippet);
    list.appendChild(item);
    resultBox.appendChild(list);
  }

  function showStatus(message, isError) {
    const statusEl = getElement("deepseek-status");
    if (!statusEl) return;
    statusEl.textContent = message;
    statusEl.classList.toggle("is-error", Boolean(isError));
  }

  function extractAnswerText(reply) {
    if (
      reply &&
      Array.isArray(reply.choices) &&
      reply.choices[0] &&
      reply.choices[0].message
    ) {
      const content = reply.choices[0].message.content;
      if (typeof content === "string") {
        return content.trim();
      }

      // 兼容可能的数组结构内容
      if (Array.isArray(content)) {
        const texts = content
          .map(function (part) {
            if (typeof part === "string") return part;
            if (part && typeof part.text === "string") return part.text;
            return "";
          })
          .filter(Boolean);
        return texts.join("\n").trim();
      }
    }

    return "";
  }

  async function queryDeepSeek(userQuery) {
    const apiKey = getApiKey();
    if (!apiKey) {
      throw new Error(
        "未配置 DeepSeek API Key，请在 script 标签设置 data-api-key。",
      );
    }

    const body = {
      model: getModel(),
      messages: [
        {
          role: "system",
          content:
            "你是 psydrugs.org 的搜索助手。请直接回答用户问题，内容清晰、准确、简洁，并尽量给出可执行建议。",
        },
        {
          role: "user",
          content: userQuery,
        },
      ],
      temperature: 0.2,
      stream: false,
    };

    const response = await fetch(getApiHost(), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + apiKey,
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(
        "DeepSeek 请求失败：" +
          response.status +
          " " +
          response.statusText +
          " " +
          text,
      );
    }

    return response.json();
  }

  async function onSearch() {
    const queryInput = getElement("deepseek-query");
    const button = getElement("deepseek-search-button");
    if (!queryInput || !button) return;

    const question = queryInput.value.trim();
    if (!question) {
      showStatus("请输入搜索关键字或问题后再查询。", true);
      return;
    }

    button.disabled = true;
    button.classList.add("is-loading");
    showStatus("正在调用 DeepSeek，请稍候…", false);

    try {
      const reply = await queryDeepSeek(question);
      const answer = extractAnswerText(reply);
      renderResult(answer);

      if (answer) {
        showStatus("查询成功。", false);
      } else {
        showStatus("返回结果为空，请尝试换个问法。", true);
      }
    } catch (error) {
      console.error("[deepseek-search] ", error);
      showStatus(
        error && error.message ? error.message : "查询失败，请检查 API 配置。",
        true,
      );
    } finally {
      button.disabled = false;
      button.classList.remove("is-loading");
    }
  }

  function attachListeners() {
    const button = getElement("deepseek-search-button");
    const queryInput = getElement("deepseek-query");
    if (!button || !queryInput) return;

    button.addEventListener("click", onSearch);
    queryInput.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();
        onSearch();
      }
    });
  }

  function applyStyles() {
    if (document.getElementById("deepseek-search-theme-style")) return;

    const style = document.createElement("style");
    style.id = "deepseek-search-theme-style";
    style.textContent = `
      .deepseek-search-wrap {
        --ds-bg: #f7f8fa;
        --ds-card-bg: #ffffff;
        --ds-border: #dfe3ea;
        --ds-text: #1f2937;
        --ds-muted: #4b5563;
        --ds-primary: #2563eb;
        --ds-primary-hover: #1d4ed8;
        --ds-status-ok: #2e7d32;
        --ds-status-err: #c62828;
      }

      @media (prefers-color-scheme: dark) {
        .deepseek-search-wrap {
          --ds-bg: #12151c;
          --ds-card-bg: #1b2230;
          --ds-border: #30394b;
          --ds-text: #e5e7eb;
          --ds-muted: #c7ced9;
          --ds-primary: #3b82f6;
          --ds-primary-hover: #60a5fa;
          --ds-status-ok: #81c784;
          --ds-status-err: #ef5350;
        }
      }

      .deepseek-search-wrap {
        max-width: 860px;
        margin: 0 auto;
        padding: 20px;
        color: var(--ds-text);
      }

      .deepseek-search-panel {
        background: var(--ds-bg);
        border: 1px solid var(--ds-border);
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 16px;
      }

      .deepseek-search-row {
        display: flex;
        gap: 10px;
        margin-bottom: 10px;
      }

      #deepseek-query {
        flex: 1;
        padding: 10px 12px;
        border: 1px solid var(--ds-border);
        border-radius: 8px;
        background: var(--ds-card-bg);
        color: var(--ds-text);
        font-size: 14px;
      }

      #deepseek-query::placeholder {
        color: var(--ds-muted);
      }

      #deepseek-search-button {
        padding: 10px 18px;
        background: var(--ds-primary);
        color: #fff;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 600;
      }

      #deepseek-search-button:hover {
        background: var(--ds-primary-hover);
      }

      #deepseek-search-button:disabled {
        opacity: 0.7;
        cursor: not-allowed;
      }

      #deepseek-status {
        min-height: 20px;
        font-size: 13px;
        color: var(--ds-status-ok);
      }

      #deepseek-status.is-error {
        color: var(--ds-status-err);
      }

      .deepseek-results-list {
        border: 1px solid var(--ds-border);
        border-radius: 10px;
        overflow: hidden;
        background: var(--ds-card-bg);
      }

      .deepseek-result-item {
        padding: 14px 16px;
      }

      .deepseek-result-title {
        font-weight: 700;
        margin-bottom: 8px;
      }

      .deepseek-result-snippet {
        margin: 0;
        color: var(--ds-text);
        white-space: pre-wrap;
        line-height: 1.7;
      }
    `;
    document.head.appendChild(style);
  }

  function init() {
    applyStyles();
    attachListeners();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
