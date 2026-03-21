from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from schemas.users import UserRequest

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    return {
      "code": 200,
      "message": "注册成功",
      "data": {
        "token": "用户访问令牌",
        "userInfo": {
          "id": 1,
          "username": user_data.username,
          "bio": "这个人很懒，什么都没有留下",
          "avatar": "https://fastly.jsdeliyr"
        }
      }
    }