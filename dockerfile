FROM python:3.10-slim AS preparation

LABEL creator="Blagovest Krasimirov Nedkov"
LABEL tags="PYTHON | FASTAPI | MONGODB | UVICORN | CELERY"
LABEL version="1.0"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED=random
ENV LANG C.UTF-8
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=10
ENV POETRY_VERSION=1.3.2
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR='/var/cache/pypoetry'

WORKDIR /one-time-secret
COPY . .

FROM preparation AS updating-and-upgrading-linux

RUN apt-get update -y && apt-get upgrade -y

FROM updating-and-upgrading-linux AS installing-packages

RUN apt-get install -y libpq-dev && apt-get install -y curl && apt-get clean -y && rm -rf /var/lib/apt/lists/*

FROM installing-packages AS installing-project-dependencies

RUN pip install poetry && poetry install --no-root