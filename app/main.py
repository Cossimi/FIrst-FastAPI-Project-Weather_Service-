from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import weather_router
from app.db.weather_db import engine, Base
from app.models import cache

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Weather API", lifespan=lifespan)
app.include_router(weather_router.router)