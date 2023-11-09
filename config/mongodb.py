from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from api.secret.models import Secret


async def get_mongo_db_client(mongo_db_url: str) -> AsyncIOMotorClient:
    """
    With motor client we can connect to specific MongoDB,
    or we can CREATE/DROP specific MongoDB.
    """
    db_client = AsyncIOMotorClient(mongo_db_url)
    return db_client


async def get_mongo_db(
    db_client: AsyncIOMotorClient, db_name: str
) -> AsyncIOMotorDatabase:
    """
    With motor db we can make a cursor connection,
    we can create or drop a mongo collections and also get specific collections.
    """
    database = db_client[db_name]
    return database


async def init_beanie_odm(database: AsyncIOMotorDatabase) -> None:
    """
    Starting BeanieODM(Object Document Mapping).
    """
    await init_beanie(database=database, document_models=[Secret])
