from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category

"""
数据库操作模块：新闻相关操作
提供对新闻分类等数据的数据库访问接口
"""

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()