from pydantic import BaseModel

#DTO
class CoordsResponse(BaseModel):
    city: str
    country: str
    lat: float
    lon: float