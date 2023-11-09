## One time secret

Welcome to my diploma work.

### About project:

This is RESTFul API (MVP) witch can help people to save there secrets
on our web service with option how much time that secret will stay "alive"
and after this will be deleted, also every secret needs to have a password
so if you want to send it on another person he will need to use this
password to open the secret.

### Language used:

- Python

### Technologies used:

- FastAPI
- MongoDB
- Docker and docker-compose
- Pydentic
- Beanie async ODM (Object Document Mapping)
- Motor async driver
- Async scheduler
- Pytest & async pytest
- HTTPX async request
- Uvicorn
- Flake8
- Coverage

### Easy run by docker:

1. Make sure you have Docker installed on your system. If not, you can download and install it from the [Docker website](https://www.docker.com/get-started).

2. Clone the repository in your local machine and open it with IDE for example on PYCharm or VSCode

3. Open a terminal and navigate to the directory where project path it is and where docker-compose-local.yml is located.

4. **Configure Your Environment**: Create a `.env` file by copying the provided `.env-example`. This file should contain sensitive information such as database settings, email configurations, and any required API keys.

    ```bash
    .env-example -> .env
    ```

5. Build the Docker image using the following command:
   ```shell
   docker-compose -f docker-compose-local.yml up

6. Done you can open [localhost](http://localhost:8000/).

