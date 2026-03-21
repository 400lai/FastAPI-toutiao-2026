from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

"""
新闻分类模型

该类定义了新闻分类的数据库模型，用于存储和管理新闻的分类信息。
包含分类ID、名称和排序序号等字段。

Attributes:
    id (int): 分类ID，主键，自增
    name (str): 分类名称，唯一且不能为空
    sort_order (int): 排序序号，默认值为0，用于控制分类显示顺序
"""
class Category(Base):
    __tablename__ = "news_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="分类ID")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="排序")

    """
    返回Category对象的字符串表示形式
    该方法用于在调试和日志记录时提供对象的可读字符串表示，

    Args:
      self: Category类的实例
    Returns:
        str: 格式化的字符串，形如"<Category(id=1, name='科技', sort_order=0)>"
    """
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"
