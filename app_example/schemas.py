from pydantic import BaseModel, ConfigDict
from typing import Optional


class AuthorCreateBase(BaseModel):
    name: str
    pseudo: str
    city: Optional[str] = None


class AuthorUpdateBase(BaseModel):
    name: Optional[str] = None
    pseudo: Optional[str] = None
    city: Optional[str] = None


class AuthorViewBase(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    pseudo: str
    city: str
