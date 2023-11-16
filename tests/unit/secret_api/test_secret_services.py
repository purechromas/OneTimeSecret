from datetime import datetime, timedelta

from api.secret.utils import (
    calculate_ttl,
    generate_random_number,
    encode_data,
    decode_data,
)


class TestSecretServices:
    def test_calculate_ttl(self):
        ttl_seconds = 3600
        current_time = datetime.utcnow()
        in_the_past = current_time + timedelta(seconds=ttl_seconds)

        in_the_future = calculate_ttl(ttl_seconds)

        assert isinstance(in_the_future, datetime) is True
        assert in_the_past < in_the_future

    def test_generate_random_number(self):
        result = generate_random_number()

        assert isinstance(result, int) is True

    def test_encode_data_and_decode_data(self):
        data = "Hey im a data"

        enc_data = encode_data(data)
        dec_data = decode_data(enc_data)

        assert data != enc_data
        assert data == dec_data
