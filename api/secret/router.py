from fastapi import APIRouter

secret_router = APIRouter(prefix='/secret', tags=['secrets'])
