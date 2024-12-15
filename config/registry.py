import logging
from app_example.models import Base
from config.database import get_engine
from app_example import controlers as example_controlers


logger = logging.getLogger("uvicorn.error")


async def init_models():
    async with get_engine().begin() as transaction:
        await transaction.run_sync(Base.metadata.create_all)
    logger.info("Tables has been created.")


def load_routers(application):
    application.include_router(router=example_controlers.router,
                                prefix="",
                                tags=["Example"])
    logger.info("Routers has been loaded.")
