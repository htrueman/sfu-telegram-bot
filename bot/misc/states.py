from aiogram.fsm.state import StatesGroup, State


class BufferForm(StatesGroup):
    opened = State()
