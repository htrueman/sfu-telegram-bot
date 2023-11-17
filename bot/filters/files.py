from aiogram.enums import ContentType
from aiogram.filters import BaseFilter
from aiogram.types import Message


class DocumentFilter(BaseFilter):
    img_ext = ("png", "jpg", "jpeg")

    async def __call__(self, message: Message) -> bool:
        return (
            message.content_type == ContentType.DOCUMENT
            and message.document.file_name.split(".")[-1] not in self.img_ext
        )


class AudioFilter(BaseFilter):
    allowed_files_content_types = (ContentType.VOICE, ContentType.AUDIO)

    async def __call__(self, message: Message) -> bool:
        return message.content_type in self.allowed_files_content_types


class VideoFilter(BaseFilter):
    allowed_files_content_types = (
        ContentType.VIDEO,
        ContentType.ANIMATION,
        ContentType.VIDEO_NOTE,
    )

    async def __call__(self, message: Message) -> bool:
        return message.content_type in self.allowed_files_content_types


class PhotoFilter(BaseFilter):
    img_ext = ("png", "jpg", "jpeg")

    allowed_files_content_types = (
        ContentType.PHOTO,
        ContentType.DOCUMENT,
    )

    async def __call__(self, message: Message) -> bool:
        if message.document is not None:
            return message.document.file_name.split(".")[-1] in self.img_ext
        return message.content_type in self.allowed_files_content_types
