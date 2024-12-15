import os
import asyncio
import pytest
import pytest_asyncio
import logging
from asgi_lifespan import LifespanManager
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.sql import text
from config.database import Base, get_db
from main import app


@pytest.fixture(scope="session")
async def async_engine():

    _engine = create_async_engine(os.getenv("DATABASE_URL_TEST"))

    async with _engine.begin() as engine:
        await engine.run_sync(Base.metadata.drop_all)
        await engine.run_sync(Base.metadata.create_all)
    logging.info("Configuration -----> Tables for testing has been created.")

    yield _engine

    async with _engine.begin() as engine:
        await engine.run_sync(Base.metadata.drop_all)
    logging.info("Configuration -----> Tables for testing has been removed.")


@pytest.fixture(scope="session")
async def async_session(async_engine) -> AsyncGenerator[AsyncSession, None]:

    _session = async_sessionmaker(
                                    autocommit=False,
                                    autoflush=False,
                                    expire_on_commit=False,
                                    bind=async_engine)
    logging.info("Configuration -----> Session created.")
    async with _session() as session:

        await session.begin()
        logging.info("Configuration -----> Session started.")
        yield session
        await session.rollback()
        logging.info("Configuration -----> Rollback executed.")
        await session.close()
        logging.info("Configuration -----> Session closed.")

        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(text(f"TRUNCATE {table.name} CASCADE;"))
            await session.commit()
        logging.info("Configuration -----> Truncate has been done.")


@pytest_asyncio.fixture(scope="session")
async def async_client(event_loop, async_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:

    def override_get_db():
        try:
            yield async_session
        finally:
            async_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    logging.info("Configuration -----> Dependency overrided.")

    async with LifespanManager(app):
       
        async with AsyncClient(
                        transport=ASGITransport(app=app),
                        base_url="http://testserver") as client:
            logging.info("Configuration -----> Client ready for running.")
            yield client
            logging.info("Configuration -----> Client finished job.")


@pytest_asyncio.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def data_test_create_author():
    return {
            "name": "JohnyG",
            "pseudo": "Walker",
            "city": "LA"}


@pytest.fixture()
def data_test_update_author():
    return {
            "pseudo": "Ranger"}
