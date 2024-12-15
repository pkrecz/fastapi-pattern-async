from fastapi import FastAPI
from config.settings import settings
from config import registry
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await registry.init_models()
    yield


def init_app():
    app = FastAPI(
                    lifespan=lifespan,
                    title=settings.title,
                    version=settings.version,
                    docs_url=settings.docs_url,
                    redoc_url=None,
                    contact={
                                "name": "Piotr",
                                "email": "pkrecz@poczta.onet.pl"})
    registry.load_routers(app)
    return app

app = init_app()
