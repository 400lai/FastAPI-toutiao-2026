from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from crud import favorite
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="api/favorite", tags=["favorite"])

@router.get("/check")
async def check_favorite(
        news_id: int = Query(..., alias = "newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    is_favorite = await favorite.is_news_favorite(db, user.username, news_id)
    # Python bool → Pydantic 对象 → FastAPI 序列化 → JSON 字符串
    return success_response(message="检查收藏状态成功", data=FavoriteCheckResponse(isFavorite = is_favorite))

@router.post("/add")
async def add_favorite(
        data: int = FavoriteAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await favorite.add_news_favorite(db, user.username, data.news_id)
    return success_response(message="添加收藏成功", data=result)

@router.delete("/remove")
async def remove_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await favorite.remove_news_favorite(db, user.id, news_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="收藏记录不存在")
    return success_response(message="删除收藏成功")