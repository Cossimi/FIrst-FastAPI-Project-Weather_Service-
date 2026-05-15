#weather_service.py

import httpx
from fastapi import HTTPException
from app.config import settings
from app.DTO.weather import WeatherResponse

class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    async def weather_service(city: str) -> WeatherResponse:
        params = {
            "q" : city,
            "appid" : settings.OPENWEATHER_API_KEY,
            "units" : "metric",
            "lang" : "ro",
        }

        #Context manager asincron pentru a asigura inchiderea conexiunii
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(WeatherService.BASE_URL, params=params)
                response.raise_for_status() #status 200(bun) daca nu err
            except httpx.HTTPStatusError as e:
                print(f"Error: {e}")
                if e.response.status_code == 404:
                    raise HTTPException(status_code=404, detail="City not found")
                raise HTTPException(status_code=500, detail="Eroare comunicare serviciu")
            except httpx.RequestError:
                raise HTTPException(status_code=500, detail="Eroare comunicare serviciu")

            #json primit
            data = response.json()

            return WeatherResponse(
                city=data["name"],
                temperature=data["main"]["temp"],
                description=data["weather"][0]["description"],
                humidity=data["main"]["humidity"])