import json
import random
from bot.application.ports import Questionnaire
from bot.domain.entity import Question
from .models import QuestionnaireData
from .mapper import to_question_entity


class JsonQuestionnaireProvider(Questionnaire):
    def __init__(self, filepath: str, image_store: str):
        self.filepath = filepath
        self.image_store = image_store
    
    def _load_storage(self) -> QuestionnaireData:
        return QuestionnaireData.parse_file(self.filepath)
    
    async def get_randome_question(self) -> Question:
        qs = []

        # Load questions list
        data = self._load_storage()
        for sec in data.sections:
            qs += sec.questions
        
        # Choice randome question
        question = random.choice(qs)
        if question.image:
            question.image = await self.get_question_image(question.image)
        return to_question_entity(question, "Test")
    
    async def get_question_image(self, code: str) -> str | bytes | None:
        # When image code is empty then return None
        if not code:
            return None
        
        # Build url
        url = self.image_store.format(code=code)
        return url

