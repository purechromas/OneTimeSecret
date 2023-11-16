from fastapi import Depends
from typing import Annotated

from api.secret.dependencies import (
    create_secret_in_db,
    review_secrets_from_db,
    review_secret_from_db,
)
from api.secret.router import secret_router
from api.secret.models import Secret
from api.secret.schemas import (
    SecretCreateOut,
    SecretReviewOut,
)


@secret_router.get("/review_secrets/", status_code=200)
async def review_secrets(
    secrets: Annotated[Secret, Depends(review_secrets_from_db)]
) -> dict:
    """
    This endpoint help us find all Secrets in our db.
    """
    return {"status": 200, "data": secrets}


@secret_router.post("/create_secret/", status_code=201)
async def create_secret(
    response: Annotated[SecretCreateOut, Depends(create_secret_in_db)]
) -> dict:
    """
    This endpoint helps us to create a secret with a specific password
    and also is generating a verification_number that we can use to find
    our secret or create a frontend client url.
    """
    return {"status": 201, "data": response}


@secret_router.post("/review_secret/{verification_number}/", status_code=200)
async def review_secret(
    secret: Annotated[SecretReviewOut, Depends(review_secret_from_db)]
) -> dict:
    """
    This endpoint is helping us find specific secret by verification number
    also to return it if password is correct, and after this to delete it,
    so it can be seen only once.
    """
    return {"detail": 200, "data": secret}
