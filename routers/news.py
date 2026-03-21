from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud import news

# 创建 APIRouter 实例
# prefix 路由前缀（API 接口规范文档）
# tags 分组 标签
router = APIRouter(prefix="/api/news", tags=["news"])

# 接口实现流程
# 1. 模块化路由 → API 接口规范文档
# 2. 定义模型类 → 数据库表（数据库设计文档）
# 3. 在 crud 文件夹里面创建文件，封装操作数据库的方法
# 4. 在路由处理函数里面调用 crud 封装好的方法，响应结果

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
        获取新闻分类列表的HTTP接口

        Args:
            skip (int, optional): 跳过的记录数，默认为0
            limit (int, optional): 返回的最大记录数，默认为100
            db (AsyncSession): 通过依赖注入获取的数据库会话对象

        Returns:
            Dict: 包含状态码、消息和数据的响应字典
                - code (int): 状态码，200表示成功
                - msg (str): 操作结果消息
                - data (List[Category]): 新闻分类数据列表
        """
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "msg": "获取新闻分类列表成功",
        "data": categories
    }

@router.get("/list")
async def get_news_list(
        category_id: int = Query(..., alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize", le=100),
        db: AsyncSession = Depends(get_db)
):
    """
        获取新闻列表的HTTP接口

        Args:
            category_id (int): 分类ID，通过查询参数传递，别名为"categoryId"
            page (int, optional): 页码，默认为1
            page_size (int, optional): 每页大小，通过查询参数传递，别名为"pageSize"，最大值为100
            db (AsyncSession): 通过依赖注入获取的数据库会话对象

        Returns:
            Dict: 包含状态码、消息和分页数据的响应字典
                - code (int): 状态码，200表示成功
                - message (str): 操作结果消息
                - data (Dict): 分页数据
                    - list (List[News]): 新闻列表
                    - total (int): 总记录数
                    - hasMore (bool): 是否还有更多数据
        """

    # 计算分页偏移量
    offset = (page - 1) * page_size
    # 查询当前页的新闻列表
    news_list = await news.get_news_list(db, category_id, offset, page_size)
    # 查询指定分类下的新闻总数
    total = await news.get_news_count(db, category_id)
    # 判断是否还有更多数据：(已跳过的数量 + 当前页数量) < 总数量
    has_more = (offset + len(news_list)) < total
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        }
    }

@router.get("/detail")
async def get_news_detail(news_id: int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    # 获取新闻详情 + 浏览量+1 + 相关新闻
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    views_res = await news.increase_news_views(db, news_detail.id)
    if not views_res:
        raise HTTPException(status_code=404, detail="新闻不存在")

    return {
      "code": 200,
      "message": "success",
      "data": {
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
        "relatedNews": "相关新闻"
      }
    }
