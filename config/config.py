from dataclasses import dataclass
from os import getenv
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str = getenv("BOT_TOKEN")
    YANDEX_WEATHER_API_KEY: str = 'bd7249d1-a738-414a-a224-32d090756c0f'
    YANDEX_GEOCODER_API_KEY: str = 'acbd6e8d-6f1f-44b5-a784-15d8cf760e15'
    WEATHER_BASE_URL: str = "https://api.weather.yandex.ru/v2/forecast"
    GEOCODER_BASE_URL: str = "https://geocode-maps.yandex.ru/1.x"