class TestSecretAPI:
    data_body = {
        "password": "YourPassword",
        "secret_msg": "YourSecretMessage",
        "ttl": 3600
    }

    async def test_get_secrets(self, async_client):
        response = await async_client.get("secret/review_secrets/")
        print(response.text)
        assert response.status_code == 200
        assert len(response.json()["data"]) == 0
        assert response.json()["status"] == 200

    async def test_post_secret(self, async_client):
        response = await async_client.post("secret/create_secret/", json=self.data_body)

        assert response.status_code == 201
        assert response.json()["status"] == 201
        assert len(response.json()["data"]) == 1

    async def test_get_secret_404_without_password(self, async_client):
        verification_number_404 = 2313213
        response_404 = await async_client.post(f"secret/review_secret/{verification_number_404}/")
        assert response_404.status_code == 404
        assert response_404.json() == {'detail': 'data not found'}

    async def test_get_secret_200_without_password(self, async_client):
        response = await async_client.post("secret/create_secret/", json=self.data_body)
        verification_number_200 = response.json()['data']['verification_number']

        response_401 = await async_client.post(f"secret/review_secret/{verification_number_200}/")
        assert response_401.status_code == 401
        assert response_401.json() == {'detail': 'unauthorized, write a password'}

    async def test_get_secret_403_with_wrong_password(self, async_client):
        response = await async_client.post("secret/create_secret/", json=self.data_body)
        verification_number_200 = response.json()['data']['verification_number']
        wrong_password = {"password": "WrongPass"}

        response_403 = await async_client.post(
            f"secret/review_secret/{verification_number_200}/", json=wrong_password
        )
        assert response_403.status_code == 403
        assert response_403.json() == {'detail': 'permission denied, wrong password'}

    async def test_get_secret_200_with_correct_password_and_404_removed(self, async_client):
        response = await async_client.post("secret/create_secret/", json=self.data_body)
        verification_number_200 = response.json()['data']['verification_number']
        correct_password = {"password": "YourPassword"}

        response_200 = await async_client.post(
            f"secret/review_secret/{verification_number_200}/", json=correct_password
        )

        assert response_200.status_code == 200
        assert response_200.json() == {'data': {'secret_msg': 'YourSecretMessage'}, 'detail': 200}

        response_404_removed = await async_client.post(
            f"secret/review_secret/{verification_number_200}/", json=correct_password
        )
        assert response_404_removed.status_code == 404
        assert response_404_removed.json() == {'detail': 'data not found'}
