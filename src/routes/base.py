from fastapi import FastAPI, APIRouter ,Depends
import os
from helpers.config import get_settings ,Settings

# MVC structure model: Model, View, Controller

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api/v1"]
)

@base_router.get("/")
async def welcome(app_settings : Settings =Depends(get_settings)):
    #app_settings = get_settings()
    app_name=app_settings.App_NAME
    app_version=app_settings.App_VERSION
    return {
        "app_name": app_name,
        "app_version": app_version
        }
        