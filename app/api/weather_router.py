#weather_router.py

from fastapi import APIRouter
from app.DTO.weather import WeatherResponse
from app.services.services import WeatherService

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/{city}", response_model=WeatherResponse)
async def get_weather(city: str):
    weather_data = await WeatherService.weather_service(city)
    return weather_data