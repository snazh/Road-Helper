from sqlalchemy import String
from sqlalchemy.orm import Mapped
from backend.src.database.connection import Base
from sqlalchemy.orm import mapped_column


# models declaration (related to Road Signs)
class RoadSign(Base):
    __tablename__ = "road_sign"
    id: Mapped[int] = mapped_column(
        unique=True, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(128), nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    image_url: Mapped[bytes] = mapped_column(
        String(length=1024), nullable=True
    )
