## Weather API

A simple weather api for getting weather information for your city.


## Setup and installation

### 1. Clone the repo
```bash
git clone https://github.com/python-way/weather-api.git
```

### 2. Set up environment variables

Create a `.env` file in the root directory by copying the example file:

```bash
cp .env.example .env
```

Now, edit the `.env` file and add your Visual Crossing Weather API key:

```
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
WEATHER_API_KEY=your-visual-crossing-api-key
```

### 3. Run the application

```bash
python weather-api.py
```
The application will be available at `http://localhost:5000`.

## API Endpoints

### Get Weather by City

*   **URL:** `/weather/<city_name>`
*   **Method:** `GET`
*   **URL Params:** `city_name=[string]` (Required)
*   **Success Response:**
    *   **Code:** 200
    *   **Content:** `{ "address": "Lucknow", "currentConditions": { ... } }`
*   **Error Response:**
    *   **Code:** 400 `Bad Request` - Invalid Location
    *   **Code:** 401 `Unauthorized` - Invalid API Key
    *   **Code:** 502 `Bad Gateway` - Failed to fetch weather data
    *   **Code:** 503 `Service Unavailable` - Weather service unavailable

### Example usage (using curl):

```bash
curl http://localhost:5000/weather/Lucknow
```

Roadmap project link:
https://roadmap.sh/projects/weather-api-wrapper-service
