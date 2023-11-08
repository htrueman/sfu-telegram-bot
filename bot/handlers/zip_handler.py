import os
import zipfile

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from magic_filter import F

from ..keyboards.inline import ZipperCallback, ZipperKeyboard
from ..misc.states import BufferForm
from ..types import ZipperOption
from ..utils import FileRemover, check_if_user_directories_have_files, zipdir

zip_router = Router()


@zip_router.message(Command("zip"))
async def zip_handler(message: Message):
    username = message.from_user.username
    await message.reply(
        text="Zip files from buffer?",
        reply_markup=ZipperKeyboard(username, [1, 2]).as_markup(),
    )


@zip_router.callback_query(ZipperCallback.filter(F.option == ZipperOption.SAVE))
async def save_callback(query: CallbackQuery, state: FSMContext):
    username = query.from_user.username
    if not check_if_user_directories_have_files(username):
        await query.answer(f"Buffer is empty! Nothing to zip.")
        return None

    zip_name = f"{username}.zip"
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipdir(zipf, username)

    await query.bot.send_document(
        chat_id=query.message.chat.id,
        document=FSInputFile(zip_name),
        reply_to_message_id=query.message.message_id,
    )
    os.remove(zip_name)

    await query.answer(f"Zipping!")


@zip_router.callback_query(ZipperCallback.filter(F.option == ZipperOption.OPEN))
async def save_callback(query: CallbackQuery, state: FSMContext):
    await state.set_state(BufferForm.opened)
    await state.set_data({BufferForm.opened: "active"})
    await query.answer(f"Buffer is open to receive your files!\n")


@zip_router.callback_query(ZipperCallback.filter(F.option == ZipperOption.CLOSE))
async def close_callback(query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    if BufferForm.opened in state_data:
        await state.clear()
        await query.answer(f"Buffer is closed! It wont receive your files.")
    await query.answer(f"Buffer is closed already!")


@zip_router.callback_query(ZipperCallback.filter(F.option == ZipperOption.CLEAR))
async def clear_callback(query: CallbackQuery):
    username = query.from_user.username
    if not check_if_user_directories_have_files(username):
        await query.answer(f"Buffer is already empty!")
        return None

    file_remover = FileRemover()
    message_data = file_remover.clear_root(username)
    message = file_remover.generate_removal_message(message_data)

    await query.answer(f"{message}")
