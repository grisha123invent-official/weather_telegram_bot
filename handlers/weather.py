from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import logging
from services.weather_api import WeatherService
from utils.formatters import format_weather_forecast
from utils.states import WeatherStates
from keyboards.inline import (
    get_interval_keyboard,
    get_route_confirmation_keyboard,
    get_location_keyboard,
    ReplyKeyboardRemove
)

# Настройка логирования
logger = logging.getLogger(__name__)

# Создаем router
router = Router()
weather_service = WeatherService()


@router.message(Command("weather"))
async def cmd_weather(message: types.Message, state: FSMContext):
    await state.set_state(WeatherStates.waiting_for_start_point)
    await message.answer(
        "🌍 Укажите начальную точку маршрута (отправьте геолокацию или введите название места)",
        reply_markup=get_location_keyboard()
    )


@router.message(WeatherStates.waiting_for_start_point)
async def process_start_point(message: types.Message, state: FSMContext):
    if message.location:
        location = f"{message.location.latitude},{message.location.longitude}"
    else:
        location = message.text

    await state.update_data(start_point=location)
    await state.set_state(WeatherStates.waiting_for_end_point)
    await message.answer(
        "📍 Теперь укажите конечную точку маршрута",
        reply_markup=get_location_keyboard()
    )


@router.message(WeatherStates.waiting_for_end_point)
async def process_end_point(message: types.Message, state: FSMContext):
    if message.location:
        location = f"{message.location.latitude},{message.location.longitude}"
    else:
        location = message.text

    await state.update_data(end_point=location)
    await state.set_state(WeatherStates.waiting_for_interval)

    # Убираем клавиатуру с геолокацией
    await message.answer(
        "⏱ Выберите интервал прогноза:",
        reply_markup=ReplyKeyboardRemove()
    )
    # Показываем инлайн-клавиатуру с интервалами
    await message.answer(
        "Выберите количество дней:",
        reply_markup=get_interval_keyboard()
    )


@router.callback_query(F.data.startswith("interval_"))
async def process_interval(callback: types.CallbackQuery, state: FSMContext):
    interval = int(callback.data.split("_")[1])
    await state.update_data(interval=interval)

    user_data = await state.get_data()
    route_text = f"""
🗺 Ваш маршрут:
- Начало: {user_data['start_point']}
- Конец: {user_data['end_point']}
- Интервал: {interval} дней

Желаете добавить промежуточные точки?
"""
    await callback.message.edit_text(
        route_text,
        reply_markup=get_route_confirmation_keyboard()
    )
    await state.set_state(WeatherStates.confirming_route)


@router.callback_query(WeatherStates.confirming_route, F.data == "route_add")
async def add_intermediate_point(callback: types.CallbackQuery, state: FSMContext):
    logger.info("Adding intermediate point...")
    await callback.message.edit_text("📍 Укажите промежуточную точку маршрута")
    await callback.message.answer(
        "Отправьте геолокацию или введите название места:",
        reply_markup=get_location_keyboard()
    )
    await state.set_state(WeatherStates.waiting_for_intermediate)


@router.message(WeatherStates.waiting_for_intermediate)
async def process_intermediate_point(message: types.Message, state: FSMContext):
    if message.location:
        location = f"{message.location.latitude},{message.location.longitude}"
    else:
        location = message.text

    # Получаем текущие данные
    data = await state.get_data()
    if 'intermediate_points' not in data:
        data['intermediate_points'] = []
    data['intermediate_points'].append(location)

    # Обновляем данные в состоянии
    await state.update_data(intermediate_points=data['intermediate_points'])

    route_text = f"""
🗺 Ваш маршрут:
- Начало: {data['start_point']}
- Промежуточные точки: {', '.join(data['intermediate_points'])}
- Конец: {data['end_point']}
- Интервал: {data['interval']} дней
"""
    # Убираем клавиатуру с геолокацией
    await message.answer(
        route_text,
        reply_markup=ReplyKeyboardRemove()
    )
    # Показываем инлайн-клавиатуру подтверждения
    await message.answer(
        "Желаете добавить еще точки?",
        reply_markup=get_route_confirmation_keyboard()
    )
    await state.set_state(WeatherStates.confirming_route)


@router.callback_query(WeatherStates.confirming_route, F.data == "route_confirm")
async def process_weather_request(callback: types.CallbackQuery, state: FSMContext):
    logger.info("Processing weather request...")
    await callback.answer("⏳ Получаю прогноз погоды...")

    user_data = await state.get_data()
    logger.info(f"User data: {user_data}")

    try:
        await callback.message.edit_text("🔄 Собираю данные о погоде...")

        weather_data = await weather_service.get_route_weather(
            start_point=user_data['start_point'],
            end_point=user_data['end_point'],
            interval=user_data['interval'],
            intermediate_points=user_data.get('intermediate_points', [])
        )

        formatted_forecast = format_weather_forecast(weather_data)
        await callback.message.edit_text(
            formatted_forecast,
            parse_mode="HTML"
        )
        logger.info("Weather forecast sent successfully")

    except Exception as e:
        logger.error(f"Error in process_weather_request: {e}", exc_info=True)
        await callback.message.edit_text(
            f"❌ Произошла ошибка при получении прогноза погоды:\n{str(e)}\n"
            "Пожалуйста, попробуйте снова позже или проверьте введённые данные."
        )

    finally:
        await state.clear()


@router.callback_query(WeatherStates.confirming_route, F.data == "route_restart")
async def restart_weather_request(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "🔄 Начинаем заново. Укажите начальную точку маршрута:"
    )
    await callback.message.answer(
        "Отправьте геолокацию или введите название места:",
        reply_markup=get_location_keyboard()
    )
    await state.set_state(WeatherStates.waiting_for_start_point)