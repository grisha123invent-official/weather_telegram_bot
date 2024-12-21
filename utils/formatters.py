def format_weather_forecast(weather_data: dict) -> str:
    """Форматирует данные о погоде в читаемый вид"""
    result = ["🌤 Прогноз погоды по маршруту:\n"]

    # Словарь для перевода погодных условий
    conditions = {
        'clear': 'ясно',
        'partly-cloudy': 'малооблачно',
        'cloudy': 'облачно',
        'overcast': 'пасмурно',
        'drizzle': 'морось',
        'light-rain': 'небольшой дождь',
        'rain': 'дождь',
        'moderate-rain': 'умеренный дождь',
        'heavy-rain': 'сильный дождь',
        'continuous-heavy-rain': 'длительный сильный дождь',
        'showers': 'ливень',
        'wet-snow': 'дождь со снегом',
        'light-snow': 'небольшой снег',
        'snow': 'снег',
        'snow-showers': 'снегопад',
        'hail': 'град',
        'thunderstorm': 'гроза',
        'thunderstorm-with-rain': 'дождь с грозой',
        'thunderstorm-with-hail': 'гроза с градом'
    }

    for location, forecasts in weather_data.items():
        result.append(f"\n📍 <b>{location}</b>")
        for date, forecast in forecasts.items():
            condition = conditions.get(forecast['condition'], forecast['condition'])
            result.append(
                f"\n{date}:"
                f"\n  🌡 Температура: {forecast['temperature']}°C"
                f"\n  🌤 Условия: {condition}"
                f"\n  💨 Ветер: {forecast['wind']} м/с"
                f"\n  ☔️ Осадки: {forecast['precipitation']} мм"
            )

    return "\n".join(result)