\# Weather API — FastAPI + PostgreSQL



An async REST API that takes a city name, geocodes it to coordinates, fetches weather data, and caches results in PostgreSQL to minimize external API calls.



\## Tech Stack



\- \*\*FastAPI\*\* — web framework for building the REST API

\- \*\*Uvicorn\*\* — ASGI server that runs the FastAPI application

\- \*\*SQLAlchemy\*\* — ORM for interacting with the database using Python classes instead of raw SQL

\- \*\*PostgreSQL\*\* — relational database used to cache weather responses for 10 minutes

\- \*\*asyncpg\*\* — async PostgreSQL driver used by SQLAlchemy under the hood

\- \*\*Pydantic\*\* — data validation and serialization via DTO models (request/response schemas)

\- \*\*httpx\*\* — async HTTP client for calling external APIs

\- \*\*python-dotenv\*\* — loads API keys and config from a `.env` file

\- \*\*unittest\*\* — unit testing with mocked external services



\## External APIs



\- \*\*Geoapify\*\* — geocoding API that converts a city name into latitude/longitude coordinates

\- \*\*OpenWeatherMap (v2.5)\*\* — weather API that returns live meteorological data given coordinates



\## Architecture



The project follows a layered architecture (equivalent to MVC):

