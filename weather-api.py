import json
import os

import requests
from flask import Flask, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis, exceptions
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
r = Redis(
            host=os.environ.get("REDIS_HOST"),
            port=os.environ.get("REDIS_PORT"),
            password=os.environ.get("REDIS_PASSWORD"),
            decode_responses=True,
        )

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=f"redis://:{os.environ.get('REDIS_PASSWORD')}@{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}",
    default_limits=["1000 per day", "100 per hour"],
)

try:
    if r.ping():
        print("Succesfully Connected to Redis Server")
except exceptions.ConnectionError as e:
    print("Redis Connection", e)
    exit(1)

API_KEY = os.environ.get("WEATHER_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"


@app.route("/")
def home():
    return redirect("/weather/Cairo")


@app.route("/weather/<string:city_name>")
@limiter.limit("1 per second")
def weather(city_name:str):

    cache_weather_data = r.get(city_name)
    if cache_weather_data:
        return json.loads(cache_weather_data), 200

    try:
        weather_request = requests.get(
                f"{BASE_URL}/{city_name}",
                params={
                    "unitGroup": "us",
                    "include": "current",
                    "key": os.environ.get("WEATHER_API_KEY"),
                    "contentType": "json",
                    },
                timeout=5,
                )

    except requests.RequestException:
        return "Failed to fetch weather data", 502

    if weather_request.status_code == 400:
        return "Invalid Locaition", 400
    elif weather_request.status_code == 401:
        return "Invalid API Key", 400
    elif not weather_request.ok:
        return "Weather service unavailable", 503

    try: 
        weather_request_data = weather_request.json()
        r.setex(city_name, 7200, json.dumps(weather_request_data))

        return weather_request_data, 200

    except request.exceptions.JSONDecodeError:
        return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
