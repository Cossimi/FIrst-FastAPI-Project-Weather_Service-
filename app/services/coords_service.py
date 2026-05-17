#coords_service

import httpx
from fastapi import HTTPException
from app.config.config import settings
from app.DTO.coords import CoordsResponse

class CoordsService:
    BASE_URL = "https://api.geoapify.com/v1/geocode/search"

    @staticmethod
    async def get_coords(city: str) -> CoordsResponse:
        params = {
            "text": city,
            "apiKey": settings.LAT_LONG_KEY,
            "limit": 1,
            "format": "json",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(CoordsService.BASE_URL, params=params)
                response.raise_for_status()
            except httpx.HTTPStatusError:
                raise HTTPException(status_code=502, detail="Eroare de serviciu")
            except httpx.RequestError:
                raise HTTPException(status_code=503, detail="Serviciul geocoding indisponibil")

            data = response.json()
            results = data.get("results",[])

            if not results:
                raise HTTPException(status_code=404, detail=f"Orasul '{city}' nu a fost gasit")
            result = results[0]
            
            return CoordsResponse(
                city=result.get("city") or result.get("name") or city,
                country=result.get("country_code", "").upper(),
                lat=result["lat"],
                lon=result["lon"],
            )