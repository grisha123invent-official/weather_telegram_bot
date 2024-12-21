import matplotlib.pyplot as plt
import folium
from io import BytesIO
import base64
from typing import List, Dict, Tuple


class VisualizationService:
    @staticmethod
    def create_temperature_graph(weather_data: Dict) -> str:
        """Создает график температуры для всех точек маршрута"""
        plt.figure(figsize=(10, 6))

        for location, forecasts in weather_data.items():
            dates = list(forecasts.keys())
            temps = [f['temperature'] for f in forecasts.values()]
            plt.plot(dates, temps, marker='o', label=location)

        plt.title('Температура по маршруту')
        plt.xlabel('Дата')
        plt.ylabel('Температура (°C)')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)

        # Сохраняем график в байты
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()

        # Кодируем в base64 для отправки в телеграм
        return base64.b64encode(buf.getvalue()).decode()

    @staticmethod
    def create_route_map(points: List[Tuple[float, float]], locations: List[str]) -> str:
        """Создает карту маршрута"""
        # Создаем карту с центром по первой точке
        m = folium.Map(location=points[0], zoom_start=10)

        # Добавляем маркеры
        for point, name in zip(points, locations):
            folium.Marker(
                point,
                popup=name,
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)

        # Соединяем точки линией
        folium.PolyLine(
            points,
            weight=2,
            color='blue',
            opacity=0.8
        ).add_to(m)

        # Сохраняем карту в байты
        buf = BytesIO()
        m.save(buf, close_file=False)
        buf.seek(0)

        return base64.b64encode(buf.getvalue()).decode()