from pydantic import BaseModel

#DTO - data transfer object
class WeatherResponse(BaseModel):
    city: str
    country: str
    latitude: float
    longitude: float
    temperature: float
    feels_like: float
    temp_min: float
    temp_max: float
    humidity: int
    pressure: int
    description: str
    icon: str
    wind_speed: float
    wind_deg: int
    clouds: int
    sunrise: int
    sunset: int
    from_cache: bool = False