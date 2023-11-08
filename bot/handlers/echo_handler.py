from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

# from aiogram.filters import StateFilter

echo_router = Router()


# @echo_router.message(F.text, StateFilter(None))
# async def bot_echo(message: types.Message):
#     text = "Send me the files and I'll zip them for you. Type /zip after the files are uploaded."
#     await message.answer(text)


@echo_router.message(F.text)
async def bot_echo_all(message: types.Message, state: FSMContext):
    text = "Send me the files and I'll zip them for you. Type /zip after the files are uploaded."
    await message.answer(text)
