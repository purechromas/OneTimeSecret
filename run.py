from fastapi import FastAPI

from api.secret.endpoints import secret_router
from config.lifespan import lifespan


def init_app() -> FastAPI:
    app = FastAPI(title="One time secret", lifespan=lifespan, docs_url="/")
    app.include_router(secret_router)

    return app


my_app: FastAPI = init_app()
