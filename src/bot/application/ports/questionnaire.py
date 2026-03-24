from typing import Protocol
from bot.domain.entity import Question


class Questionnaire(Protocol):
    async def get_randome_question(self) -> Question: ...
    async def get_question_image(self, code: str) -> str | bytes: ...
