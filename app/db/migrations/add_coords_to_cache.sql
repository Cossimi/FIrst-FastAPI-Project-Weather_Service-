#migration1
ALTER TABLE weather_cache
    ADD COLUMN latitude  FLOAT,
    ADD COLUMN longitude FLOAT;