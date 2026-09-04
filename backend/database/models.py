from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from .connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    watchlists = relationship(
        "Watchlist",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Watchlist(Base):
    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String(20), nullable=False, index=True)
    company_name = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_viewed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="watchlists")

    snapshots = relationship(
        "StockSnapshot",
        back_populates="watchlist",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "symbol",
            name="unique_user_stock"
        ),
    )


class StockSnapshot(Base):
    __tablename__ = "stock_snapshots"

    id = Column(Integer, primary_key=True, index=True)

    watchlist_id = Column(
        Integer,
        ForeignKey("watchlists.id"),
        nullable=False,
        index=True
    )

    symbol = Column(String(20), nullable=False, index=True)
    price = Column(Float, nullable=False)
    previous_close = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    watchlist = relationship(
        "Watchlist",
        back_populates="snapshots"
    )


class NewsEvent(Base):
    __tablename__ = "news_events"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(1000), nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    __tablename__ = "news_events"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)

    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(1000), nullable=True)
    published_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )