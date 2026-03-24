from typing import Optional
from pydantic import BaseModel


class Question(BaseModel):
    question: str
    image: Optional[str]
    options: list[str]
    right_idx: list[int]

class SectionQuestions(BaseModel):
    title: str
    questions: list[Question]
    count: int

class QuestionnaireData(BaseModel):
    total_count_sections: int
    total_count_qs: int
    sections: list[SectionQuestions]
