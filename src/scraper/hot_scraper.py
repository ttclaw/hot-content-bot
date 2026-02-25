#!/usr/bin/env python3
"""
热点爬虫模块
支持：微博热搜、知乎热榜
"""

import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

import requests
from bs4 import BeautifulSoup


class BaseScraper:
    """爬虫基类"""
    
    def __init__(self, name: str, source_url: str):
        self.name = name
        self.source_url = source_url
        self.data_dir = Path(__file__).parent.parent.parent / "data" / "raw"
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def fetch(self) -> List[Dict]:
        """抓取数据，子类实现"""
        raise NotImplementedError
    
    def save(self, data: List[Dict]):
        """保存数据"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.name}_{timestamp}.json"
        filepath = self.data_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"[+] 已保存 {len(data)} 条数据到 {filepath}")
        return filepath


class WeiboScraper(BaseScraper):
    """微博热搜爬虫"""
    
    def __init__(self):
        super().__init__("weibo", "https://s.weibo.com/top/summary")
    
    def fetch(self) -> List[Dict]:
        """抓取微博热搜"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        try:
            resp = requests.get(self.source_url, headers=headers, timeout=10)
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            hot_list = []
            table = soup.find('table', {'class': 'rank-table'})
            
            if table:
                rows = table.find_all('tr')[1:]  # 跳过表头
                for i, row in enumerate(rows[:50], 1):  # 前50条
                    tds = row.find_all('td')
                    if len(tds) >= 2:
                        rank = tds[0].text.strip()
                        topic_elem = tds[1].find('a')
                        if topic_elem:
                            title = topic_elem.text.strip()
                            url = 'https://s.weibo.com' + topic_elem.get('href', '')
                            
                            # 提取热度
                            heat_elem = tds[1].find('span', {'class': 'hot-num'})
                            heat = heat_elem.text.strip() if heat_elem else "0"
                            
                            hot_list.append({
                                'rank': i,
                                'title': title,
                                'url': url,
                                'heat': heat,
                                'source': 'weibo',
                                'fetched_at': datetime.now().isoformat()
                            })
            
            return hot_list
            
        except Exception as e:
            print(f"[-] 微博抓取失败: {e}")
            return []


class ZhihuScraper(BaseScraper):
    """知乎热榜爬虫"""
    
    def __init__(self):
        super().__init__("zhihu", "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total")
    
    def fetch(self) -> List[Dict]:
        """抓取知乎热榜"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'https://www.zhihu.com/hot'
        }
        
        try:
            resp = requests.get(self.source_url, headers=headers, timeout=10)
            data = resp.json()
            
            hot_list = []
            items = data.get('data', [])
            
            for i, item in enumerate(items[:50], 1):
                target = item.get('target', {})
                title = target.get('title', '')
                url = target.get('url', '')
                
                # 提取热度（回答数/浏览量）
                metrics = {
                    'answer_count': target.get('answer_count', 0),
                    'follower_count': target.get('follower_count', 0),
                    'visit_count': item.get('detail_text', '')
                }
                
                hot_list.append({
                    'rank': i,
                    'title': title,
                    'url': url,
                    'metrics': metrics,
                    'source': 'zhihu',
                    'fetched_at': datetime.now().isoformat()
                })
            
            return hot_list
            
        except Exception as e:
            print(f"[-] 知乎抓取失败: {e}")
            return []


def fetch_all():
    """抓取所有数据源"""
    scrapers = [WeiboScraper(), ZhihuScraper()]
    
    for scraper in scrapers:
        print(f"\n[*] 正在抓取: {scraper.name}")
        data = scraper.fetch()
        if data:
            scraper.save(data)
        time.sleep(2)  # 礼貌延迟


if __name__ == "__main__":
    fetch_all()
