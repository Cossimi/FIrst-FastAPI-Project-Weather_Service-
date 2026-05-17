import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.owm_service import OWMService
from app.DTO.coords import CoordsResponse
from app.DTO.weather import WeatherResponse
from fastapi import HTTPException
import httpx


class TestOWMService(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # date de test
        self.geo = CoordsResponse(
            city="Iasi",
            country="RO",
            lat=47.1585,
            lon=27.6014
        )

        self.mock_owm_response = {
            "main": {
                "temp": 18.5,
                "feels_like": 17.0,
                "temp_min": 16.0,
                "temp_max": 20.0,
                "humidity": 60,
                "pressure": 1013
            },
            "weather": [{"description": "cer senin", "icon": "01d"}],
            "wind": {"speed": 3.5, "deg": 180},
            "clouds": {"all": 0},
            "sys": {"country": "RO", "sunrise": 1715742000, "sunset": 1715793600}
        }

    async def test_get_owm_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_owm_response
        mock_response.raise_for_status = MagicMock()

        with patch("app.services.owm_service.httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )

            result = await OWMService.get_owm(self.geo)

            self.assertIsInstance(result, WeatherResponse)
            self.assertEqual(result.city, "Iasi")
            self.assertEqual(result.country, "RO")
            self.assertEqual(result.temperature, 18.5)
            self.assertEqual(result.humidity, 60)
            self.assertFalse(result.from_cache)

    async def test_get_owm_invalid_api_key(self):
        mock_response = MagicMock()
        mock_response.status_code = 401

        http_error = httpx.HTTPStatusError(
            "401 Unauthorized",
            request=MagicMock(),
            response=mock_response
        )

        with patch("app.services.owm_service.httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                side_effect=http_error
            )

            with self.assertRaises(HTTPException) as ctx:
                await OWMService.get_owm(self.geo)

            self.assertEqual(ctx.exception.status_code, 401)

    async def test_get_owm_service_unavailable(self):
        with patch("app.services.owm_service.httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                side_effect=httpx.RequestError("Timeout")
            )

            with self.assertRaises(HTTPException) as ctx:
                await OWMService.get_owm(self.geo)

            self.assertEqual(ctx.exception.status_code, 503)


if __name__ == "__main__":
    unittest.main()