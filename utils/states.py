from aiogram.fsm.state import State, StatesGroup

class WeatherStates(StatesGroup):
    waiting_for_start_point = State()
    waiting_for_end_point = State()
    waiting_for_interval = State()
    waiting_for_intermediate = State()
    confirming_route = State()