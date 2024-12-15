from sqlalchemy import Column, Integer, String
from config.database import Base


class AuthorModel(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    pseudo = Column(String(100), unique=True, nullable=False)
    city = Column(String(100), nullable=False)
