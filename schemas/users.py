from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
    """
    用户请求数据模型
    用于接收用户注册或登录时提交的请求数据，包含用户名和密码。
   """
    username: str
    password: str


# user_info 对应的类：基础类 + Info 类（id、用户名）
class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型

    定义用户基本信息字段的验证规则和约束，被 UserInfoResponse 继承使用。
    所有字段均为可选，用于用户信息的部分更新和完整响应。

    Attributes:
        nickname (Optional[str]): 用户昵称，最大长度 50 字符
        avatar (Optional[str]): 用户头像 URL，最大长度 255 字符
        gender (Optional[str]): 用户性别，最大长度 10 字符
        bio (Optional[str]): 用户个人简介，最大长度 500 字符
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")


class UserInfoResponse(UserInfoBase):
    """
    用户信息响应数据模型
    继承自 UserInfoBase，用于 API 响应中返回完整的用户信息。
    包含用户的基础信息（昵称、头像、性别、个人简介）以及 ID 和用户名。
    """
    id: int
    username: str

    # 模型配置：支持从 ORM 对象属性加载数据
    model_config = ConfigDict(
        from_attributes=True  # 允许通过属性访问 ORM 模型数据
    )


class UserAuthResponse(BaseModel):
    """
    用户认证响应数据模型

    用于返回用户认证后的响应数据，包含访问令牌和用户详细信息。
    Attributes:
        token (str): 访问令牌，用于后续请求的身份验证
        user_info (UserInfoResponse): 用户信息响应对象，包含用户的基本信息和详细资料
    """
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    # 模型配置：支持字段别名和 ORM 对象属性映射
    model_config = ConfigDict(
        populate_by_name=True,  # 允许通过字段名或别名访问
        from_attributes=True  # 支持从 ORM 模型属性加载数据
    )

class UserUpdateRequest(BaseModel):
    """
    用户信息更新请求数据模型
    用于接收用户提交的信息更新请求，所有字段均为可选，支持部分更新。
    """
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None

class UserChangePasswordRequest(BaseModel):
    """
    用户修改密码请求数据模型
    Attributes:
       old_password (str): 用户的当前密码（旧密码），用于验证身份
       new_password (str): 用户的新密码，最小长度为 6 个字符
    """
    old_password: str = Field(..., alias="oldPassword", description="旧密码")
    new_password: str = Field(..., min_length=6, alias="newPassword", description="新密码")

