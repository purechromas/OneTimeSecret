from datetime import datetime, timezone

from api.secret.models import Secret


async def find_expired_secrets() -> None:
    current_datetime = datetime.now(timezone.utc)
    await Secret.find(Secret.ttl < current_datetime).delete()
