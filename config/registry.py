import logging
from config.database import Base, get_engine
from app_example import controlers as example_controlers


logger = logging.getLogger("uvicorn.error")


async def init_models():
    async with get_engine().begin() as transaction:
        await transaction.run_sync(Base.metadata.create_all)
    logger.info("Tables has been created.")


def load_routers(application):
    application.include_router(
                                router=example_controlers.router,
                                prefix="",
                                tags=["Example"])
    logger.info("Routers has been loaded.")
