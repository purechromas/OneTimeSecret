from datetime import datetime

from beanie import Document, Indexed


class Secret(Document):
    secret_msg: str
    password: str
    verification_number: Indexed(int)
    ttl: datetime
    created_at: datetime

    class Settings:
        name = "secrets-collection"
