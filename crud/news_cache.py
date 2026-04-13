from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import get_cached_categories, set_cached_categories, get_cache_news_list, set_cache_news_list
from models.news import Category, News
from schemas.base import NewsItemBase

"""
数据库操作模块：新闻相关操作
提供对新闻分类等数据的数据库访问接口
"""

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # 先尝试从缓存中获取数据
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()    # ORM类型
    # 写入缓存
    if categories:
        categories = jsonable_encoder(categories)
        await set_cached_categories(categories)

    # 返回数据
    return categories


async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    # 先尝试从缓存中获取新闻数据
    # 跳过的数量skip = (页码 - 1) * 每页数量 -> 页码 = 跳过的数量 / 每页数量 + 1
    page = skip // limit + 1

    cached_news_list = await get_cache_news_list(category_id, page, limit)  # 缓存数据json
    if cached_news_list:
        # 将缓存中的JSON数据转换为News对象列表并返回
        return [News(**item) for item in cached_news_list]
    # 查询的是指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    # 写入缓存
    if news_list:
        # 先把 ORM 数据转换为 字典才能写入缓存
        # ORM 转成 Pydantic,再转为 字典
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
        await set_cache_news_list(category_id, page, limit, news_data)

    return news_list

async def get_news_count(db: AsyncSession, category_id: int):
    # 查询的是指定分类下的新闻数量
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  # 只能有一个结果，否则报错

async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 更新 → 检查数据库是否真的命中了数据 → 命中了返回True
    return result.rowcount > 0

async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    # 构建查询语句：查找同一分类下且非当前新闻的其他新闻
    # 按阅读量和发布时间降序排列，并限制返回数量
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.views.desc(),  # 阅读量降序
        News.publish_time.desc()  # 发布时间降序
    ).limit(limit)
    # 执行数据库查询
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    # 使用列表推导式提取相关新闻的核心数据字段并返回
    return [{
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views
    } for news_detail in related_news]
