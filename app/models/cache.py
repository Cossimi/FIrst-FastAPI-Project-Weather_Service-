#cache

from app.db.weather_db import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

class WeatherCache(Base):
    __tablename__ = "weather_cache"

    id          = Column(Integer, primary_key=True, index=True)
    city        = Column(String(100), index=True)
    country     = Column(String(10))
    latitude    = Column(Float) #migration1
    longitude   = Column(Float) #migration1
    temperature = Column(Float)
    feels_like  = Column(Float)
    temp_min    = Column(Float)
    temp_max    = Column(Float)
    humidity    = Column(Integer)
    pressure    = Column(Integer)
    description = Column(String(200))
    icon        = Column(String(20))
    wind_speed  = Column(Float)
    wind_deg    = Column(Integer)
    clouds      = Column(Integer)
    sunrise     = Column(Integer)
    sunset      = Column(Integer)
    cached_at   = Column(DateTime(timezone=True), server_default=func.now())