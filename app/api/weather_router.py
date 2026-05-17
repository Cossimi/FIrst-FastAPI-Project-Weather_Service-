#weather_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.weather_db import get_db
from app.DTO.weather import WeatherResponse
from app.services.weather_service import WeatherService

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/{city}", response_model=WeatherResponse)
async def get_weather(city: str, db: AsyncSession = Depends(get_db)):
    return await WeatherService.get_weather(city, db)