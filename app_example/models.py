from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from config.database import Base


class AuthorModel(Base):

    __tablename__ = "author"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    pseudo: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)