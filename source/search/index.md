---
title: AI 智能搜索
date: 2026-05-03
layout: page
cover: https://gcore.jsdelivr.net/gh/cdn-x/xaoxuu@main/posts/20250706150531375.jpg
---
# Deepseek-R1 智能搜索

<div style="max-width: 800px; margin: 0 auto; padding: 20px;">
  <div style="margin-bottom: 30px;">
    <h4>在全站内容中使用 AI 进行语义搜索。当前使用模型为：deepseek-r1:1.5b</h4>
  </div>

  <div style="background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
    <div style="display: flex; gap: 10px; margin-bottom: 15px;">
      <input 
        id="deepseek-query" 
        type="text" 
        placeholder="输入问题或关键词，例如：右美沙芬的用法、苯二氮卓的风险..."
        style="flex: 1; padding: 10px 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;"
      />
      <button 
        id="deepseek-search-button"
        style="padding: 10px 20px; background: #2196F3; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: 500;"
      >
        搜索
      </button>
    </div>
    <div id="deepseek-status" style="min-height: 20px; font-size: 13px;"></div>
  </div>

  <div id="deepseek-results" style="min-height: 100px;"></div>
</div>

<script src="/js/deepseek-search.js" data-api-host="http://127.0.0.1:11434/api/generate"></script>
