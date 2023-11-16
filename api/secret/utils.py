import random
from datetime import datetime, timedelta

from config.settings import cipher_suite


def calculate_ttl(ttl_sec: int) -> datetime:
    """
    Counting how much time will live a specific secret document.
    """
    time_to_live = datetime.utcnow() + timedelta(seconds=ttl_sec)
    return time_to_live


def generate_random_number() -> int:
    """
    Generate a random number witch we use to check if there is a specific secret in your database.
    """
    number = int("".join(str(random.randint(1, 9)) for _ in range(8)))
    return number


def encode_data(data: str) -> str:
    """
    The function is used to make our db data to not be human-readable.
    """
    encoded_data = cipher_suite.encrypt(data.encode())
    return encoded_data


def decode_data(data: str) -> str:
    """
    The function is used to convert db data to a human-readable data.
    """
    decoded_data = cipher_suite.decrypt(data).decode()
    return decoded_data
