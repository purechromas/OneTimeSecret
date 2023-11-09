import base64
import hashlib
import os
from datetime import timezone
from cryptography.fernet import Fernet
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

from api.secret.task import find_expired_secrets

# Loading all
load_dotenv()

# Secret app key
SECRET_KEY: str = os.getenv("SECRET_KEY")

# App settings
DEBUG: bool = True
HOST: str = "localhost"
PORT: int = 8000

# MongoDB local
MONGO_DB_USERNAME: str = os.getenv("MONGO_DB_USERNAME")
MONGO_DB_PASSWORD: str = os.getenv("MONGO_DB_PASSWORD")
REAL_MONGO_DB_NAME: str = os.getenv("REAL_MONGO_DB_NAME")
TEST_MONGO_DB_NAME: str = os.getenv("TEST_MONGO_DB_NAME")
MONGO_DB_LOCAL_URL_DOCKER: str = (
    f"mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@mongodb:27017"
)
MONGO_DB_LOCAL_URL_TEST: str = (
    f"mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@localhost:27017"
)

# MongoDB cloud
MONGO_DB_CLOUD_URL: str = os.getenv("MONGO_DB_CLOUD_URL")

if DEBUG:
    MONGO_DB_URL = MONGO_DB_LOCAL_URL_DOCKER
else:
    MONGO_DB_URL = MONGO_DB_CLOUD_URL

# Encoder-Decoder settings
KEY = base64.urlsafe_b64encode(hashlib.sha256(SECRET_KEY.encode()).digest())
cipher_suite = Fernet(KEY)

# Async Scheduler settings
scheduler = AsyncIOScheduler()
scheduler.add_job(
    find_expired_secrets,
    CronTrigger(hour=23, minute=0, second=0, timezone=timezone.utc),
)
