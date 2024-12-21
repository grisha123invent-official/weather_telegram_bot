from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def get_interval_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="3 дня", callback_data="interval_3")
    builder.button(text="5 дней", callback_data="interval_5")
    builder.button(text="7 дней", callback_data="interval_7")
    builder.adjust(3)  # Размещаем кнопки в один ряд по 3 штуки
    return builder.as_markup()

def get_route_confirmation_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Подтвердить", callback_data="route_confirm")
    builder.button(text="➕ Добавить точку", callback_data="route_add")
    builder.button(text="🔄 Начать заново", callback_data="route_restart")
    builder.adjust(1, 2)  # Первая кнопка отдельно, остальные две в ряд
    return builder.as_markup()

def get_location_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="📍 Отправить местоположение", request_location=True)],
        [KeyboardButton(text="↩️ Ввести вручную")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)