from datetime import datetime

from sqlalchemy import String, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.database.connection import Base


# models declaration (related to Users)
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        unique=True, primary_key=True
    )
    username: Mapped[str] = mapped_column(
        String(length=64), unique=True, nullable=False
    )
    registered_at: Mapped[datetime] = mapped_column(  # todo: replace deprecated time method
        TIMESTAMP, default=datetime.utcnow
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    avatar: Mapped[str] = mapped_column(
        String, default=None, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )




