from bot.domain.entity import Question
from .models import Question as QuestionDTO


def to_question_entity(question: QuestionDTO, section_name: str) -> Question:
    return Question.new(
        question=question.question,
        section_name=section_name,
        options=question.options,
        right_answer_idx=question.right_idx,
        image_code=question.image,
        explanation=None
    )
