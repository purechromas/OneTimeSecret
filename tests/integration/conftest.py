import asyncio
import pytest
from httpx import AsyncClient
from config.mongodb import get_mongo_db_client, get_mongo_db, init_beanie_odm
from config.settings import MONGO_DB_LOCAL_URL_TEST, TEST_MONGO_DB_NAME
from run import init_app


@pytest.fixture(scope="session")
def event_loop():
    """
    We are using event loop coz async def fixtures can't work without it.
    """
    return asyncio.get_event_loop()


@pytest.fixture(scope="session", autouse=True)
async def create_and_drop_test_db() -> None:
    """
    We are using MotorDriver and BeanieODM for creating a connection
    and init a db before we start the session and after session we drop the db.
    """
    db_client = await get_mongo_db_client(mongo_db_url=MONGO_DB_LOCAL_URL_TEST)
    database = await get_mongo_db(db_client=db_client, db_name=TEST_MONGO_DB_NAME)

    await init_beanie_odm(database=database)
    yield
    await db_client.drop_database(TEST_MONGO_DB_NAME)


@pytest.fixture(scope="session")
async def async_client() -> AsyncClient:
    """
    We are using HTTPX client witch can work with ASGI as our FASTAPI app.
    With this client we can send a restful request methods and check our api.
    """
    my_app = init_app()

    async with AsyncClient(app=my_app, base_url="http://test") as ac:
        yield ac
