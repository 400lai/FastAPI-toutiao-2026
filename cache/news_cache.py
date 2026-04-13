# 新闻相关的缓存方法、新闻分类的读取和写入
from typing import Any

from config.cache_config import get_json_cache, set_cache

CATEGORIES_KEY = "news:categories"

# 获取新闻分类缓存

async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)

# 写入新闻分类缓存：缓存的数据、过期时间
# 分类、配置 7200；列表 600;详情 1800；验证码 120 -- 数据越稳定，缓存越持久
async def set_cached_categories(data: list[dict[str, Any]], expire: int = 3600 * 2):
    return await set_cache(CATEGORIES_KEY, data, expire)