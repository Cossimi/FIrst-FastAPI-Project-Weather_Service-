#config.py

import os
from dotenv import load_dotenv

load_dotenv()
class Settings:
    def __init__(self):
        self.OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
        self.LAT_LONG_KEY        = os.getenv("LAT_LONG_KEY", "")
        self.DATABASE_URL        = os.getenv("DATABASE_URL", "")
        self.CACHE_TTL_MINUTES   = int(os.getenv("CACHE_TTL_MINUTES", 30))

        if not self.OPENWEATHER_API_KEY:
            raise ValueError("OPENWEATHER_API_KEY lipseste din .env")
        if not self.LAT_LONG_KEY:
            raise ValueError("LAT_LONG_KEY lipseste din .env")
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL lipseste din .env")
settings = Settings()