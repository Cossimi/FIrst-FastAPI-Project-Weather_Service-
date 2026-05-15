#config.py

import os
from dotenv import load_dotenv

load_dotenv()
class Settings:
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", None)

def __post_init__(self):
    if not self.OpenWeatherAPI_KEY:
        raise ValueError("API key not provided")
settings = Settings()