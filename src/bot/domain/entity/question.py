from typing import Optional, List
from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    question: str
    section_name: str
    image_code: Optional[str]
    options: List[str]
    explanation: Optional[str]
    right_answer_idx: List[int]

    @classmethod
    def new(cls,
            question: str,
            section_name: str,
            options: List[str],
            right_answer_idx: List[int],
            explanation: Optional[str] = None,
            image_code: Optional[str] = None
        ):
        if not right_answer_idx:
            raise ValueError("param \"right_answer_idx\" cannot be empty")
        if not options:
            raise ValueError("param \"options\" cannot be empty")
        if right_answer_idx[-1] >= len(options):
            raise IndexError("param \"right_answer_idx\" range out")

        return Question(
            question=question,
            section_name=section_name,
            image_code=image_code,
            options=options,
            explanation=explanation,
            right_answer_idx=right_answer_idx
        )