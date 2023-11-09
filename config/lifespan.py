from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from config.mongodb import get_mongo_db_client, get_mongo_db, init_beanie_odm
from config.settings import scheduler, REAL_MONGO_DB_NAME, MONGO_DB_URL


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """
    This generator helps us to init all app dependencies
    like (MONGODB-DRIVER, BEANIE ODM, ASYNC-SCHEDULER) when we run FASTAPI
    and also to close them when we stop FASTAPI.
    This helps our app to work correctly.
    """
    # Start the scheduler when the app starts
    scheduler.start()

    # Initialize MongoDB using the provided mongo_url and mongo_name
    db_client: AsyncIOMotorClient = await get_mongo_db_client(mongo_db_url=MONGO_DB_URL)
    database: AsyncIOMotorDatabase = await get_mongo_db(
        db_client=db_client, db_name=REAL_MONGO_DB_NAME
    )
    await init_beanie_odm(database=database)
    yield

    # Shutdown the scheduler when the app is shutting down
    scheduler.shutdown()
