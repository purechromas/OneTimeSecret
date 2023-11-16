from datetime import datetime
from typing import Annotated

from fastapi import Path, Body, HTTPException

from api.secret.models import Secret
from api.secret.schemas import SecretCreateIn, SecretCreateOut, SecretReviewIn, SecretReviewOut
from api.secret.utils import encode_data, calculate_ttl, generate_random_number, decode_data


async def get_secrets_from_db() -> list[Secret]:
    secrets = await Secret.find_all().to_list()
    return secrets


async def create_secret_in_db(
        request: Annotated[SecretCreateIn, Body]
) -> SecretCreateOut:
    ttl_sec = request.ttl

    secret = await Secret(
        secret_msg=encode_data(request.secret_msg),
        password=encode_data(request.password),
        ttl=calculate_ttl(ttl_sec),
        verification_number=generate_random_number(),
        created_at=datetime.utcnow(),
    ).create()

    response = SecretCreateOut(verification_number=secret.verification_number)

    return response


async def get_secret_from_db(
        verification_number: Annotated[int | None, Path],
        request: Annotated[SecretReviewIn | None, Body] = None
) -> SecretReviewOut:
    secret = await Secret.find_one(Secret.verification_number == verification_number)

    if not request:
        if not secret:
            raise HTTPException(status_code=404, detail="data not found")
        raise HTTPException(status_code=401, detail="unauthorized, write a password")
    else:
        if not secret:
            raise HTTPException(status_code=404, detail="data not found")
        if request.password != decode_data(secret.password):
            raise HTTPException(
                status_code=403, detail="permission denied, wrong password"
            )

        response = SecretReviewOut(secret_msg=decode_data(secret.secret_msg))
        await secret.delete()

        return response
