from pydantic import BaseModel

#DTO - data transfer object
class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    humidity: int