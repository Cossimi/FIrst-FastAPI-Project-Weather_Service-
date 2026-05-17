#weather_service.py
import httpx
from fastapi import HTTPException
from app.DTO.coords import CoordsResponse
from app.config.config import settings
from app.DTO.weather import WeatherResponse

class OWMService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    async def get_owm(geo: CoordsResponse) -> WeatherResponse:
        params = {
            "lat":   geo.lat,
            "lon":   geo.lon,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric",
            "lang":  "ro",
            "format": "json",
        }

        #Context manager asincron pentru a asigura inchiderea conexiunii
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(OWMService.BASE_URL, params=params)
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    raise HTTPException(status_code=401, detail="API key OWM invalid")
                raise HTTPException(status_code=502, detail="Eroare serviciu meteo")
            except httpx.RequestError:
                raise HTTPException(status_code=503, detail="Serviciul meteo nu este disponibil")

            #json primit
            data = response.json()

            return WeatherResponse(
                city = geo.city,
                country = geo.country,
                latitude = geo.lat,
                longitude = geo.lon,
                temperature=data["main"]["temp"],
                feels_like = data["main"]["feels_like"],
                temp_min=data["main"]["temp_min"],
                temp_max=data["main"]["temp_max"],
                humidity = data["main"]["humidity"],
                pressure = data["main"]["pressure"],
                description = data["weather"][0]["description"],
                icon = data["weather"][0]["icon"],
                wind_speed = data["wind"]["speed"],
                wind_deg = data["wind"].get("deg", 0),
                clouds = data["clouds"]["all"],
                sunrise = data["sys"]["sunrise"],
                sunset = data["sys"]["sunset"],
                from_cache=False,
            )
