import aiohttp
from typing import List, Dict, Any, Tuple
from config.config import Config


class WeatherService:
    def __init__(self):
        self.weather_url = Config.WEATHER_BASE_URL
        self.geocoder_url = Config.GEOCODER_BASE_URL
        self.weather_api_key = Config.YANDEX_WEATHER_API_KEY
        self.geocoder_api_key = Config.YANDEX_GEOCODER_API_KEY

    async def get_coordinates(self, location: str) -> Tuple[float, float]:
        """Получает координаты по названию места через Яндекс Геокодер"""
        async with aiohttp.ClientSession() as session:
            params = {
                "apikey": self.geocoder_api_key,
                "format": "json",
                "geocode": location
            }

            async with session.get(self.geocoder_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    try:
                        pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
                        lon, lat = map(float, pos.split())
                        return lat, lon
                    except (KeyError, IndexError):
                        raise Exception(f"Не удалось найти координаты для {location}")
                else:
                    raise Exception(f"Ошибка геокодирования: {response.status}")

    async def get_weather(self, lat: float, lon: float, days: int = 3) -> Dict:
        """Получает прогноз погоды от Яндекс.Погоды"""
        headers = {
            "X-Yandex-API-Key": self.weather_api_key
        }
        params = {
            "lat": lat,
            "lon": lon,
            "limit": days,
            "hours": "false",
            "extra": "false"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    self.weather_url,
                    headers=headers,
                    params=params
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Ошибка получения погоды: {response.status}")

    async def get_route_weather(
            self,
            start_point: str,
            end_point: str,
            interval: int,
            intermediate_points: List[str] = None
    ) -> Dict[str, Any]:
        """Получает прогноз погоды для всех точек маршрута"""
        if intermediate_points is None:
            intermediate_points = []

        points = [start_point] + intermediate_points + [end_point]
        weather_data = {}

        for point in points:
            try:
                if ',' in point:
                    lat, lon = map(float, point.split(','))
                else:
                    lat, lon = await self.get_coordinates(point)

                forecast = await self.get_weather(lat, lon, interval)
                weather_data[point] = self._parse_forecast(forecast)
            except Exception as e:
                raise Exception(f"Ошибка при получении данных для {point}: {str(e)}")

        return weather_data

    def _parse_forecast(self, forecast_data: Dict) -> Dict[str, Dict]:
        """Парсит ответ от API Яндекс.Погоды в удобный формат"""
        result = {}

        for forecast in forecast_data.get('forecasts', []):
            date = forecast['date']
            result[date] = {
                'temperature': forecast['parts']['day']['temp_avg'],
                'condition': forecast['parts']['day']['condition'],
                'wind': forecast['parts']['day']['wind_speed'],
                'precipitation': forecast['parts']['day']['prec_mm']
            }

        return result