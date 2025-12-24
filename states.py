from aiogram.fsm.state import StatesGroup, State


class PairAddingStates(StatesGroup):
    pair_name = State()
    exchange_name = State()


class ParamsChangingStates(StatesGroup):
    pair_id = State()
    page = State()
    growth_rate = State()
    correction_rate = State()
    candle_count = State()
