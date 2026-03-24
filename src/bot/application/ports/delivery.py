from typing import Protocol
from bot.domain.entity import Question
from bot.application.dto import OutboundMessage


class Delivery(Protocol):
    async def send_question(self, question: Question) -> bool: ...
    async def send_to_channel(self, message: OutboundMessage) -> bool: ...
