from aiogram import Router
from aiogram.enums import ContentType
from aiogram.types import Message

from ..utils import DocumentDownloader, PhotoDownloader
from ..filters.files import DocumentFilter, AudioFilter, VideoFilter, PhotoFilter
from ..misc.states import BufferForm

file_router = Router()


@file_router.message(BufferForm.opened, DocumentFilter())
async def document_downloader(message: Message):
    await DocumentDownloader(message, ContentType.DOCUMENT).download()


@file_router.message(BufferForm.opened, AudioFilter())
async def audio_downloader(message: Message):
    await DocumentDownloader(message, ContentType.AUDIO).download()


@file_router.message(BufferForm.opened, VideoFilter())
async def video_downloader(message: Message):
    await DocumentDownloader(message, ContentType.VIDEO).download()


@file_router.message(BufferForm.opened, PhotoFilter())
async def photo_downloader(message: Message):
    if message.content_type == ContentType.DOCUMENT:
        await DocumentDownloader(message, ContentType.PHOTO).download()
    else:
        await PhotoDownloader(message, ContentType.PHOTO).download()
