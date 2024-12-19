from typing import TypeVar, Annotated
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi_filter.contrib.sqlalchemy import Filter
from config.database import Base


Model = TypeVar("Model", bound=Base)


class CrudOperationRepository:

    def __init__(self, db: AsyncSession, model: Model):
        self.db = db
        self.model = model


    async def get_by_id(self, id: int) -> Model:
        return await self.db.get(self.model, id)


    async def get_all(self, filter: Filter = None) -> Model:
        query = select(self.model)
        if filter is not None:
            query = filter.filter(query)
            query = filter.sort(query)
        instance = await self.db.scalars(query)
        return instance.all()


    async def create(self, record: Model) -> Model:
        self.db.add(record)
        await self.db.flush()
        await self.db.refresh(record)
        return record


    async def update(self, record: Model, data: Annotated[BaseModel, dict]) -> Model:
        if isinstance(data, BaseModel):
            data = data.model_dump(exclude_none=True)
        for key, value in data.items():
            setattr(record, key, value)
        await self.db.flush()
        await self.db.refresh(record)
        return record


    async def delete(self, record: Model) -> bool:
        if record is not None:
            await self.db.delete(record)
            await self.db.flush()
            return True
        else:
            return False


    async def retrieve(self, record: Model) -> Model:
        return record


    async def list(self, record: Model) -> list[Model]:
        return record
