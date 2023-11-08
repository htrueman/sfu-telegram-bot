from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hcode

from ..filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())
user_router = Router()


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply(f"Hello, admin {hcode(message.from_user.username)}!")


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply(f"Hello, user {hcode(message.from_user.username)}!")
