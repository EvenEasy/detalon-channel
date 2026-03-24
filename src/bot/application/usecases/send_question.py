from bot.domain.entity import Question
from bot.application.ports import Questionnaire, Delivery


class SendQuestionToChatUseCase:
    def __init__(self, delivery: Delivery, questionnaire: Questionnaire):
        self.delivery = delivery
        self.questionnaire = questionnaire

    async def execute(self):
        question = await self.questionnaire.get_randome_question()
        await self.delivery.send_question(question)