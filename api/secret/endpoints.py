from datetime import datetime
from fastapi.exceptions import HTTPException

from api.secret.router import secret_router
from api.secret.models import Secret
from api.secret.schemas import SecretCreateIn, SecretCreateOut, SecretReviewIn, SecretReviewOut
from api.secret.services import calculate_ttl, generate_random_number, encode_data, decode_data


@secret_router.get("/review_secrets/", status_code=200)
async def review_secrets() -> dict:
    """
    This endpoint help us find all Secrets in our db.
    """
    secrets = await Secret.find_all().to_list()
    return {"status": 200, "data": secrets}


@secret_router.post("/create_secret/", status_code=201)
async def create_secret(request: SecretCreateIn) -> dict:
    """
    This endpoint helps us to create a secret with a specific password
    and also is generating a verification_number that we can use to find
    our secret or create a frontend client url.
    """
    ttl_sec = request.ttl

    secret = await Secret(
        secret_msg=encode_data(request.secret_msg),
        password=encode_data(request.password),
        ttl=calculate_ttl(ttl_sec),
        verification_number=generate_random_number(),
        created_at=datetime.utcnow()
    ).create()

    response = SecretCreateOut(verification_number=secret.verification_number)

    return {"status": 201, "data": response}


@secret_router.post("/review_secret/{number}/", status_code=200)
async def review_secret(number: int, request: SecretReviewIn | None = None) -> dict:
    """
    This endpoint is helping us find specific secret by verification number
    also to return it if password is correct, and after this to delete it,
    so it can be seen only once.
    """
    secret = await Secret.find_one(Secret.verification_number == number)
    if not request:
        if not secret:
            raise HTTPException(status_code=404, detail="data not found")
        raise HTTPException(status_code=401, detail="unauthorized, write a password")
    else:
        if not secret:
            raise HTTPException(status_code=404, detail="data not found")
        if request.password != decode_data(secret.password):
            raise HTTPException(status_code=403, detail="permission denied, wrong password")

        response = SecretReviewOut(secret_msg=decode_data(secret.secret_msg))
        await secret.delete()

        return {"detail": 200, "data": response}
