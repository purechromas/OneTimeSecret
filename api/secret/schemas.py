from pydantic import BaseModel


class SecretCreateIn(BaseModel):
    secret_msg: str
    password: str
    ttl: int  # Time to live: in seconds

    class Config:
        json_schema_extra = {
            "example": {
                "secret_msg": "YourSecretMessage",
                "password": "YourPassword",
                "ttl": 3600,
            }
        }


class SecretCreateOut(BaseModel):
    verification_number: int


class SecretReviewIn(BaseModel):
    password: str


class SecretReviewOut(BaseModel):
    secret_msg: str
