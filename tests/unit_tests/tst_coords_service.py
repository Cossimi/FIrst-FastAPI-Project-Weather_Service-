import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.coords_service import CoordsService
from app.DTO.coords import CoordsResponse
from fastapi import HTTPException

class TestCoordsService(unittest.TestCase):
    async def test_get_coords_success(self):
        #raspuns corect de la Geoapify
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {
            "results": [
                {
                    "city": "Iași",
                    "country_code": "RO",
                    "lat": 47.1585,
                    "lon": 27.6014
                }
            ]
        }

        mock_response.raise_for_status = MagicMock

        with patch("app.services.coords_service.httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )

        result = await CoordsService.get_coords("Iași")

        self.assertIsInstance(result, CoordsResponse)
        self.assertEqual(result.city, "Iași")
        self.assertEqual(result.country, "RO")
        self.assertEqual(result.lat, 47.1585)
        self.assertEqual(result.lon, 27.6014)

    async def test_get_coords_city_not_found(self):
        #raspuns inexistent de la Geoapify
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = MagicMock()

        with patch("app.services.coords_service.httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )

            with self.assertRaises(HTTPException) as context:
                await CoordsService.get_coords("MockCity")

            self.assertEqual(context.exception.status_code, 404)

    async def test_get_coords_service_unavailable(self):
        # Simulam eroare de retea
        import httpx
        with patch("app.services.coords_service.httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                side_effect=httpx.RequestError("Connection failed")
            )

            with self.assertRaises(HTTPException) as ctx:
                await CoordsService.get_coords("Iasi")

            self.assertEqual(ctx.exception.status_code, 503)


if __name__ == "__main__":
    unittest.main()