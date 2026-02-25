# 内容生成服务 - 配置文件

# 数据源配置
SOURCES = {
    "weibo": {
        "name": "微博热搜",
        "url": "https://s.weibo.com/top/summary",
        "enabled": True,
        "fetch_interval": 300,  # 5分钟
    },
    "zhihu": {
        "name": "知乎热榜", 
        "url": "https://www.zhihu.com/hot",
        "enabled": True,
        "fetch_interval": 600,  # 10分钟
    },
    "xiaohongshu": {
        "name": "小红书热门",
        "url": "https://www.xiaohongshu.com/explore",
        "enabled": False,  # 需要登录，第二阶段
        "fetch_interval": 900,
    },
    "jike": {
        "name": "即刻热门",
        "url": "https://web.okjike.com",
        "enabled": False,  # 需要API，第二阶段
        "fetch_interval": 600,
    }
}

# 内容生成配置
GENERATION = {
    "models": {
        "fast": "kimi-k2",      # 快速生成短内容
        "deep": "kimi-k2.5",    # 深度分析长文
    },
    "content_types": {
        "flash": {  # 快讯
            "max_length": 500,
            "style": "简洁、有冲击力、适合社交媒体",
        },
        "analysis": {  # 深度分析
            "max_length": 2000,
            "style": "专业、有洞察、有数据支撑",
        },
        "visual": {  # 可视化
            "type": "chart",
            "tools": ["matplotlib", "wordcloud"],
        }
    }
}

# 发布平台配置
PLATFORMS = {
    "wechat": {  # 公众号
        "enabled": False,
        "app_id": "",
        "app_secret": "",
    },
    "xiaohongshu": {  # 小红书
        "enabled": False,
        "cookies": "",
    },
    "jike": {  # 即刻
        "enabled": False,
        "api_key": "",
    }
}

# 定时任务配置
SCHEDULE = {
    "fetch_hot": "*/10 * * * *",      # 每10分钟抓取热点
    "generate_flash": "0 * * * *",     # 每小时生成快讯
    "generate_analysis": "0 9,15,21 * * *",  # 每天3次深度分析
    "publish": "0 */2 * * *",          # 每2小时检查发布队列
}
