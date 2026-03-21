from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Index, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

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

class News(Base):
    # 数据库表名定义
    __tablename__ = "news"

    # 数据库表索引配置
    # 为提高查询性能，在常用查询字段上创建索引：
    __table_args__ = (
        Index('fk_news_category_idx', 'category_id'),  # 优化分类查询性能（高频查询场景）
        Index('idx_publish_time', 'publish_time')  # 优化按发布时间排序的查询性能
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻ID")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻标题")
    description: Mapped[Optional[str]] = mapped_column(String(500), comment="新闻简介")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(String(255), comment="封面图片URL")
    author: Mapped[Optional[str]] = mapped_column(String(50), comment="作者")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_category.id'), nullable=False, comment="分类ID")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="发布时间")

    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', views={self.views})>"
