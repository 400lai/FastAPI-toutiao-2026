from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class NewsItemBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int = Field(alias="categoryId")
    views: int
    publish_time: Optional[datetime] = Field(None, alias="publishedTime")

    # 模型配置：支持字段别名和 ORM 对象属性映射
    model_config = ConfigDict(
        populate_by_name=True,  # 允许通过字段名或别名访问
        from_attributes=True  # 支持从 ORM 模型属性加载数据
    )