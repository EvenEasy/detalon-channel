from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from bot.application.dto import (
    OutboundMessage,
    OutboundTextMessage,
    OutboundPhotoMessage,
    OutboundPollMessage
)
from bot.application.ports import Delivery
from bot.domain.entity.question import Question
from .mapper import TelegramQuestionMapper

class TelegramDelivery(Delivery):
    def __init__(self, bot_token: str, channel_id: int):
        self._bot = Bot(bot_token, default=DefaultBotProperties(parse_mode='HTML'))
        self._channel_id = channel_id
        self._mapper = TelegramQuestionMapper()
    
    async def send_question(self, question: Question) -> bool:
        messages = self._mapper.map(question)

        for message in messages:
            await self.send_to_channel(message)
        return True
    
    async def send_to_channel(self, message: OutboundMessage) -> bool:
        match message:
            case OutboundTextMessage():
                await self._send_text(message)

            case OutboundPhotoMessage():
                await self._send_photo(message)

            case OutboundPollMessage():
                await self._send_poll(message)

            case _:
                raise TypeError(f"Unsupported outbound message type: {type(message).__name__}")
        return True

    async def _send_text(self, message: OutboundTextMessage) -> None:
        await self._bot.send_message(
            chat_id=self._channel_id,
            text=message.text,
            reply_markup=message.keyboard,
        )

    async def _send_photo(self, message: OutboundPhotoMessage) -> None:
        await self._bot.send_photo(
            chat_id=self._channel_id,
            photo=message.photo_code,
            caption=message.caption,
            reply_markup=message.keyboard
        )

    async def _send_poll(self, message: OutboundPollMessage) -> None:
        options = message.options or []
        if len(options) < 2:
            raise ValueError("Poll must contain at least 2 options")

        send_kwargs = {
            "chat_id": self._channel_id,
            "question": message.question,
            "options": options,
            "is_anonymous": True,
            "correct_option_id": message.correct_option_id,
            #"allows_multiple_answers": message.allows_multiple_answers,
            "type": 'quiz'
        }

        #if message.type == "quiz":
        #    send_kwargs["correct_option_id"] = message.correct_option_id
        #    send_kwargs["explanation"] = message.explanation

        await self._bot.send_poll(**send_kwargs)
