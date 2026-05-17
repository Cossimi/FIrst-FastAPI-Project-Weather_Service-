from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone, timedelta

from app.config.config import settings
from app.DTO.weather import WeatherResponse
from app.models.cache import WeatherCache
from app.services.coords_service import CoordsService
from app.services.owm_service import OWMService

class WeatherService:

    @staticmethod
    async def get_weather(city: str, db: AsyncSession) -> WeatherResponse:

        # 1. Cauta in cache
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=settings.CACHE_TTL_MINUTES)
        result = await db.execute(
            select(WeatherCache)
            .where(WeatherCache.city == city.lower())
            .where(WeatherCache.cached_at >= cutoff)
            .order_by(WeatherCache.cached_at.desc())
        )
        cached = result.scalars().first()

        if cached:
            return WeatherResponse(
                city=cached.city,
                country=cached.country,
                latitude=cached.latitude,
                longitude=cached.longitude,
                temperature=cached.temperature,
                feels_like=cached.feels_like,
                temp_min=cached.temp_min,
                temp_max=cached.temp_max,
                humidity=cached.humidity,
                pressure=cached.pressure,
                description=cached.description,
                icon=cached.icon,
                wind_speed=cached.wind_speed,
                wind_deg=cached.wind_deg,
                clouds=cached.clouds,
                sunrise=cached.sunrise,
                sunset=cached.sunset,
                from_cache=True,
            )

        # 2. Coords
        geo = await CoordsService.get_coords(city)

        # 3. Date meteo
        weather = await OWMService.get_owm(geo)

        # 4. Salveaza in cache
        entry = WeatherCache(
            city=city.lower(),
            country=weather.country,
            latitude=weather.latitude,
            longitude=weather.longitude,
            temperature=weather.temperature,
            feels_like=weather.feels_like,
            temp_min=weather.temp_min,
            temp_max=weather.temp_max,
            humidity=weather.humidity,
            pressure=weather.pressure,
            description=weather.description,
            icon=weather.icon,
            wind_speed=weather.wind_speed,
            wind_deg=weather.wind_deg,
            clouds=weather.clouds,
            sunrise=weather.sunrise,
            sunset=weather.sunset,
        )
        db.add(entry)
        await db.commit()

        return weather