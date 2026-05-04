---
title: AI 智能搜索
date: 2026-05-03
layout: page
cover: https://gcore.jsdelivr.net/gh/cdn-x/xaoxuu@main/posts/20250706150531375.jpg
---
# DeepSeek 智能搜索

<div class="deepseek-search-wrap">
  <div style="margin-bottom: 18px;">
    <h4>在全站内容中使用 AI 语义搜索。当前模型：DeepSeek API（deepseek-chat）</h4>
  </div>

  <div class="deepseek-search-panel">
    <div class="deepseek-search-row">
      <input
        id="deepseek-query"
        type="text"
        placeholder="输入问题或关键词，例如：右美沙芬的用法、苯二氮卓的风险..."
      />
      <button id="deepseek-search-button">搜索</button>
    </div>
    <div id="deepseek-status"></div>
  </div>

  <div id="deepseek-results" style="min-height: 100px;"></div>
</div>

<script
  src="/js/deepseek-search.js"
  data-api-key="sk-2f15bf1d72444fefb8456932c7c70534"
  data-api-host="https://api.deepseek.com/v1/chat/completions"
  data-model="deepseek-chat"
></script>
