from aiogram import Router
from aiogram.enums import ContentType
from aiogram.filters import invert_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup

from ..keyboards.inline import ClearBufferKeyboard
from ..types import DownloaderOptionString, DownloaderOption
from ..utils import DocumentDownloader, PhotoDownloader
from ..filters.files import DocumentFilter, AudioFilter, VideoFilter, PhotoFilter
from ..misc.states import BufferForm

file_router = Router()


async def on_startup_buffer_check(
    message: Message,
    state: FSMContext,
    downloader_option: DownloaderOptionString,
    content_type: ContentType,
) -> None:
    state_data = await state.get_data()
    if state_data.get("buffer_initialized") is None:
        await state.set_state(BufferForm.opened)
        await state.set_data({"buffer_initialized": True, BufferForm.opened: "active"})
        if downloader_option == DownloaderOption.DOCUMENT:
            await DocumentDownloader(message, get_keyboard(message), content_type).download()
        else:
            await PhotoDownloader(message,  get_keyboard(message), content_type).download()


@file_router.message(invert_f(BufferForm.opened), DocumentFilter())
async def document_downloader_buffer_init(message: Message, state: FSMContext):
    await on_startup_buffer_check(
        message,
        state,
        downloader_option=DownloaderOption.DOCUMENT,
        content_type=ContentType.DOCUMENT,
    )


@file_router.message(invert_f(BufferForm.opened), AudioFilter())
async def audio_downloader_buffer_init(message: Message, state: FSMContext):
    await on_startup_buffer_check(
        message,
        state,
        downloader_option=DownloaderOption.DOCUMENT,
        content_type=ContentType.AUDIO,
    )


@file_router.message(invert_f(BufferForm.opened), VideoFilter())
async def video_downloader_buffer_init(message: Message, state: FSMContext):
    await on_startup_buffer_check(
        message,
        state,
        downloader_option=DownloaderOption.DOCUMENT,
        content_type=ContentType.VIDEO,
    )


@file_router.message(invert_f(BufferForm.opened), PhotoFilter())
async def photo_downloader_buffer_init(message: Message, state: FSMContext):
    if message.content_type == ContentType.DOCUMENT:
        await on_startup_buffer_check(
            message,
            state,
            downloader_option=DownloaderOption.DOCUMENT,
            content_type=ContentType.PHOTO,
        )
    else:
        await on_startup_buffer_check(
            message,
            state,
            downloader_option=DownloaderOption.PHOTO,
            content_type=ContentType.PHOTO,
        )


@file_router.message(BufferForm.opened, DocumentFilter())
async def document_downloader(message: Message):
    await DocumentDownloader(message, get_keyboard(message), ContentType.DOCUMENT).download()


@file_router.message(BufferForm.opened, AudioFilter())
async def audio_downloader(message: Message):
    await DocumentDownloader(message, get_keyboard(message), ContentType.AUDIO).download()


@file_router.message(BufferForm.opened, VideoFilter())
async def video_downloader(message: Message):
    await DocumentDownloader(message, get_keyboard(message), ContentType.VIDEO).download()


@file_router.message(BufferForm.opened, PhotoFilter())
async def photo_downloader(message: Message):
    if message.content_type == ContentType.DOCUMENT:
        await DocumentDownloader(message, get_keyboard(message), ContentType.PHOTO).download()
    else:
        await PhotoDownloader(message, get_keyboard(message), ContentType.PHOTO).download()


def get_keyboard(message: Message) -> InlineKeyboardMarkup:
    username = message.from_user.username
    return ClearBufferKeyboard(username).as_markup()

