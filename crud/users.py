from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from schemas.users import UserRequest
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
