from datetime import datetime, timezone

from api.secret.models import Secret


async def find_expired_secrets() -> None:
    """
    Every night at 00:00 AsyncScheduler from settings.py is running this function,
    witch is finding all expired secrets and delete them.
    """
    current_datetime = datetime.now(timezone.utc)
    await Secret.find(Secret.ttl < current_datetime).delete()
