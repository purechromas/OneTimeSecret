import base64
import hashlib
from datetime import timezone
from pathlib import Path
from cryptography.fernet import Fernet
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

from api.secret.task import find_expired_secrets

BASE_DIR: Path = Path(__file__).resolve().parent.parent


class ConfigSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / '.env', env_file_encoding='utf-8', extra='ignore')


class AppSettings(ConfigSettings):
    SECRET_KEY: str = Field(alias="APP_SECRET_KEY")
    DEBUG: bool = True
    HOST: str = "localhost"
    PORT: int = 8001


class MongoSettings(ConfigSettings):
    USERNAME: str = Field(alias='MONGO_USERNAME')
    PASSWORD: str = Field(alias='MONGO_PASSWORD')
    REAL_DB_NAME: str = Field(alias='MONGO_REAL_DB_NAME')
    TEST_DB_NAME: str = Field(alias='MONGO_TEST_DB_NAME')
    URL_CLOUD: str = Field(alias="MONGO_URL_CLOUD")
    URL_LOCAL: str = Field(default=None, validate_default=False)
    URL_DOCKER: str = Field(default=None, validate_default=False)

    def __init__(self):
        super().__init__()
        self.URL_LOCAL = f"mongodb://{self.USERNAME}:{self.PASSWORD}@localhost:27017"
        self.URL_DOCKER = f"mongodb://{self.USERNAME}:{self.PASSWORD}@mongodb:27017"


class Settings(BaseSettings):
    APP: AppSettings = AppSettings()
    MONGO: MongoSettings = MongoSettings()


settings = Settings()

# Encoder-Decoder settings
KEY = base64.urlsafe_b64encode(hashlib.sha256(settings.APP.SECRET_KEY.encode()).digest())
cipher_suite = Fernet(KEY)

# Async Scheduler settings
scheduler = AsyncIOScheduler()
scheduler.add_job(
    find_expired_secrets,
    CronTrigger(hour=0, minute=0, second=0, timezone=timezone.utc),
)
