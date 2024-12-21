from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот прогноза погоды для вашего маршрута.\n"
        "Я помогу узнать погоду в точках вашего путешествия.\n"
        "Используйте /help для получения списка команд."
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
🌤 Доступные команды:
/start - Начать работу с ботом
/help - Показать это сообщение
/weather - Запросить прогноз погоды для маршрута

Для получения прогноза погоды:
1. Отправьте команду /weather
2. Укажите начальную точку маршрута
3. Укажите конечную точку маршрута
4. Выберите временной интервал прогноза
5. При желании добавьте промежуточные точки
"""
    await message.answer(help_text)