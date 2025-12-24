from aiogram.filters import BaseFilter
from aiogram.types import Message

import filters


class IsAdmin(BaseFilter):
    def __init__(self, chat_id: int | list[int]) -> None:
        self.chat_id = chat_id

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.chat_id, int):
            return message.from_user.id == self.chat_id
        return message.from_user.id in self.chat_id


class IsNewbie(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if await filters.user_exists(message.from_user.id):
            return False
        return True
