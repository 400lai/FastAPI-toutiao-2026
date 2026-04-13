from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias = "isFavorite")

class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias = "newsId")

# 规划两个类： 一个是新闻模型类 + 收藏的模型类
class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id: int = Field(alias="favoriteId")
    favorite_time: datetime = Field(alias="favoriteTime")

    # 模型配置：支持字段别名和 ORM 对象属性映射
    model_config = ConfigDict(
        populate_by_name=True,  # 允许通过字段名或别名访问
        from_attributes=True  # 支持从 ORM 模型属性加载数据
    )

# 收藏列表接口响应模型类
class FavoriteListResponse(BaseModel):
    list: list[FavoriteNewsItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    # 模型配置：支持字段别名和 ORM 对象属性映射
    model_config = ConfigDict(
        populate_by_name=True,  # 允许通过字段名或别名访问
        from_attributes=True  # 支持从 ORM 模型属性加载数据
    )