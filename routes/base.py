from fastapi import FASTAPI, APIRouter

base_router = APIRouter()

@base_router.get("/")
def welcome():
    return {
        "message": "Welcome to mini-RAG!"
        }
    