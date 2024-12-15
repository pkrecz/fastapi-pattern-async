from typing import Type, TypeVar
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi_filter.contrib.sqlalchemy import Filter


Model = TypeVar("Model", bound=SQLModel)


class CrudOperationRepository:

    def __init__(self, db: AsyncSession, model: type[Model]):
        self.db = db
        self.model = model

    async def get_by_id(self, id: int) -> Type[Model]:
        return await self.db.get(self.model, id)

    async def get_all(self, filter: Filter = None) -> Type[Model]:
        query = select(self.model)
        if filter is not None:
            query = filter.filter(query)
            query = filter.sort(query)
        instances = await self.db.execute(query)
        return instances.scalars().all()

    async def create(self, record: Type[Model]) -> Type[Model]:
        self.db.add(record)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def update(self, record: Type[Model], data) -> Type[Model]:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(record, key, value)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def delete(self, record: Type[Model]) -> bool:
        if record is not None:
            await self.db.delete(record)
            await self.db.flush()
            return True
        else:
            return False

    async def retrieve(self, record: Type[Model]) -> Type[Model]:
        return record

    async def list(self, record: Type[Model]) -> list[Type[Model]]:
        return record
