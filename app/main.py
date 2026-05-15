from fastapi import FastAPI
from app.api import weather_router

app = FastAPI(title="Weather API")
app.include_router(weather_router.router)