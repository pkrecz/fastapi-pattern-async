from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class AuthorModel(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    pseudo = Column(String(100), unique=True, nullable=False)
    city = Column(String(100), nullable=False)
