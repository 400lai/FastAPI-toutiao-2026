from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from crud import users
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 注册逻辑：验证用户是否存在 -> 创建用户 → 生成 Token  → 响应结果
    # 检查用户名是否已被注册
    existing_user = await users.get_user_by_username(db, user_data.username)
    # 用户名已存在时抛出 400 错误请求异常
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")

    # 创建新用户并保存到数据库
    user = await users.create_user(db, user_data)
    # 为新用户生成访问令牌
    token = await users.create_token(db, user.id)
    # return {
    #   "code": 200,
    #   "message": "注册成功",
    #   "data": {
    #     "token": token,
    #     "userInfo": {
    #       "id": user.id,
    #       "username": user.username,
    #       "bio": user.bio,
    #       "avatar": user.avatar
    #     }
    #   }
    # }
    # 构建认证响应数据：包含访问令牌和完整的用户信息
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))

    # 返回标准化的成功响应，包含注册成功消息和用户认证数据
    return success_response(message="注册成功", data=response_data)

@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 登录逻辑：验证用户是否存在 -> 验证密码 -> 生成 Token  → 响应结果
    # 执行用户身份认证，验证用户名和密码
    user = await users.authenticate_user(db, user_data.username, user_data.password)

    # 认证失败时抛出 401 未授权异常
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    # 为认证通过的用户生成访问令牌
    token = await users.create_token(db, user.id)

    # 构建认证响应数据：包含访问令牌和完整的用户信息
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    # 返回标准化的成功响应，包含登录成功消息和用户认证数据
    return success_response(message="登录成功啦", data=response_data)