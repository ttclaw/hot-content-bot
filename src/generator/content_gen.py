#!/usr/bin/env python3
"""
内容生成模块
使用 Kimi API 生成热点分析内容
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class ContentGenerator:
    """内容生成器"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.processed_dir = self.data_dir / "processed"
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def load_latest_hot(self, source: str) -> List[Dict]:
        """加载最新的热点数据"""
        raw_dir = self.data_dir / "raw"
        files = sorted(raw_dir.glob(f"{source}_*.json"), reverse=True)
        
        if not files:
            return []
        
        with open(files[0], 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_flash(self, hot_items: List[Dict], count: int = 5) -> str:
        """
        生成热点快讯（短内容）
        适合：小红书、即刻、朋友圈
        """
        # 选择热度最高的几条
        top_items = hot_items[:count]
        
        prompt = f"""你是一个热点资讯博主，请根据以下热点生成一条社交媒体快讯。

热点列表：
{json.dumps([{"title": item["title"], "heat": item.get("heat", "N/A")} for item in top_items], ensure_ascii=False)}

要求：
1. 总字数控制在 300-500 字
2. 开头要有吸引力，用 emoji 或悬念
3. 每条热点用 1-2 句话概括核心看点
4. 结尾加一句互动引导（提问或投票）
5. 语气轻松、有网感，适合小红书/即刻风格

输出格式：
[标题]
[正文]
[互动引导]
"""
        
        # 这里调用 Kimi API
        # 暂时返回模板
        content = self._generate_with_kimi(prompt)
        return content
    
    def generate_analysis(self, hot_item: Dict) -> str:
        """
        生成深度分析（长文）
        适合：公众号、知乎专栏
        """
        prompt = f"""你是一个深度内容创作者，请对以下热点进行深度分析。

热点：{hot_item['title']}

要求：
1. 总字数 1500-2000 字
2. 结构：现象描述 → 背景分析 → 深层原因 → 影响预测 → 个人观点
3. 要有数据支撑或案例引用
4. 观点要有洞察，不随大流
5. 语言专业但不晦涩

输出格式：
# [标题]

## 发生了什么

## 为什么重要

## 深层逻辑

## 后续影响

## 我的看法
"""
        
        content = self._generate_with_kimi(prompt)
        return content
    
    def _generate_with_kimi(self, prompt: str) -> str:
        """
        调用 Kimi API 生成内容
        注：实际部署时需要配置 API Key
        """
        # 这里集成 Kimi API 调用
        # 暂时返回占位符
        return f"[Kimi 生成内容占位符]\n\nPrompt:\n{prompt[:200]}..."
    
    def save_content(self, content: str, content_type: str, source: str):
        """保存生成的内容"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{content_type}_{source}_{timestamp}.md"
        filepath = self.processed_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[+] 已保存内容: {filepath}")
        return filepath


def generate_daily():
    """生成每日内容"""
    gen = ContentGenerator()
    
    # 生成快讯
    for source in ["weibo", "zhihu"]:
        hot_items = gen.load_latest_hot(source)
        if hot_items:
            print(f"\n[*] 生成 {source} 快讯")
            content = gen.generate_flash(hot_items)
            gen.save_content(content, "flash", source)


if __name__ == "__main__":
    generate_daily()
