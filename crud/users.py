import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.sync import update

from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
from utils import security


async def get_user_by_username(db: AsyncSession, username: str):
    """
    根据用户名查询用户信息

    :param db: 异步数据库会话对象
    :param username: 待查询的用户名
    :return: 如果找到则返回 User 对象，否则返回 None
    """
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserRequest):
    """
    创建新用户并保存到数据库

    :param db: 异步数据库会话对象
    :param user_data: 用户请求数据，包含用户名和密码等信息
    :return: 创建成功后的 User 对象
    """
    # 对密码进行哈希加密处理
    hashed_password = security.get_hash_password(user_data.password)
    # 创建 User 实例对象
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)            # 将用户对象添加到数据库会话
    await db.commit()       # 提交事务，保存到数据库
    await db.refresh(user)  # 从数据库刷新用户对象的最新数据
    return user             # 返回创建的用户对象

# 生成 Token
async def create_token(db: AsyncSession, user_id: int):
    # 生成 Token + 设置过期时间 → 查询数据库当前用户是否有 Token → 有：更新；没有：添加
    token = str(uuid.uuid4())
    # 设置 Token 过期时间为 7 天后
    expires_at = datetime.now() + timedelta(days=7)
    # 查询用户是否已有 Token 记录
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        # 已有记录则更新 Token 和过期时间
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        # 无记录则创建新的 Token 记录并提交
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)

    await db.commit()
    return token

async def authenticate_user(db: AsyncSession, username: str, password: str):
    # 根据用户名查询用户信息
    user = await get_user_by_username(db, username)

    # 用户不存在时返回 None
    if not user:
        return None
    # 验证密码是否匹配
    if not security.verify_password(password, user.password):
        return None

    # 认证成功，返回用户对象
    return user


# 根据 Token 查询用户：验证 Token → 查询用户
async def get_user_by_token(db: AsyncSession, token: str):
    # 根据 Token 查询数据库中的 Token 记录
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()

    # Token 不存在或已过期时返回 None
    if not db_token or db_token.expires_at < datetime.now():
        return None

    # Token 有效，根据 user_id 查询关联的用户信息
    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 更新用户信息: update更新 → 检查是否命中 → 获取更新后的用户返回
async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    # update(User).where(User.username == username).values(字段=值, 字段=值)
    # user_data 是一个Pydantic类型，得到字典 → ** 解包
    # 构建动态更新语句，仅更新请求中明确设置且非空的字段
    query = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    ))

    # 执行更新语句并提交数据库事务
    result = await db.execute(query)
    await db.commit()

    # 验证更新结果，无受影响行说明用户不存在
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 查询并返回更新后的用户完整信息
    updated_user = await get_user_by_username(db, username)
    return updated_user

# 修改密码: 验证旧密码 → 新密码加密 → 修改密码
async def change_password(db: AsyncSession, user: User, old_password: str, new_password: str):
    # 验证旧密码是否正确，不匹配则返回 False
    if not security.verify_password(old_password, user.password):
        return False

    # 对新密码进行 bcrypt 哈希加密
    hashed_new_pwd = security.get_hash_password(new_password)
    # 更新用户对象的密码字段为加密后的新密码
    user.password = hashed_new_pwd

    # 将用户对象添加到会话并提交，确保 SQLAlchemy 跟踪变更并持久化
    db.add(user)        # 避免 session 过期或关闭导致的提交失败问题
    await db.commit()   # 刷新用户对象状态，获取数据库中的最新值
    await db.refresh(user)
    return True
