from typing import Type, TypeVar
from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_filter.contrib.sqlalchemy import Filter
from .models import AuthorModel
from .repository import CrudOperationRepository


Model = TypeVar("Model", bound=SQLModel)


class AuthorService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = AuthorModel
        self.crud = CrudOperationRepository(self.db, self.model)

    async def author_create(self, data: Type[BaseModel]) -> Type[Model]:
        instance = self.model(**data.model_dump())
        return await self.crud.create(instance)

    async def author_update(self, id: int, data: Type[BaseModel]) -> Type[Model]:
        instance = await self.crud.get_by_id(id)
        return await self.crud.update(instance, data)

    async def author_delete(self, id: int) -> bool:
        instance = await self.crud.get_by_id(id)
        return await self.crud.delete(instance)

    async def author_retrieve(self, id: int) -> Type[Model]:
        instance = await self.crud.get_by_id(id)
        return await self.crud.retrieve(instance)

    async def author_list(self, filter: Filter = None) -> Type[Model]:
        instances = await self.crud.get_all(filter)
        return await self.crud.list(instances)
