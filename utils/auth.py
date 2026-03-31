from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from crud import users


# 整合 根据 Token 查询用户，返回用户
async def get_current_user(
        authorization: str = Header(..., alias="Authorization"),
        db: AsyncSession = Depends(get_db)
):
    # Bearer xxxxx
    # 去除 "Bearer " 前缀，提取纯 Token 字符串
    token = authorization.replace("Bearer ", "")

    # 根据 Token 验证并查询用户信息
    user = await users.get_user_by_token(db, token)

    # Token 无效或已过期时抛出 401 未授权异常
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌或已经过期的令牌")

    return user
