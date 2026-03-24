from typing import Optional

from bot.application.dto import (
    OutboundMessage,
    OutboundTextMessage,
    OutboundPhotoMessage,
    OutboundPollMessage,
)
from bot.domain.entity.question import Question


class TelegramQuestionMapper:
    TEXT_LIMIT = 4096
    PHOTO_CAPTION_LIMIT = 1024

    POLL_QUESTION_LIMIT = 300
    POLL_OPTION_LIMIT = 100
    POLL_OPTIONS_MIN = 2
    POLL_OPTIONS_MAX = 12
    QUIZ_EXPLANATION_LIMIT = 200
    QUIZ_EXPLANATION_MAX_NEWLINES = 2

    OPTION_LABELS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

    def map(self, question: Question) -> list[OutboundMessage]:
        self._validate_question(question)

        if self._can_send_as_single_poll(question):
            return [self._build_full_poll(question)]

        use_full_options_in_poll = self._can_use_full_options_in_poll(question)

        content_message = self._build_content_message(
            question=question,
            include_options_text=not use_full_options_in_poll,
        )
        poll_message = self._build_compact_poll(question=question)
        return [content_message, poll_message]

    def _validate_question(self, question: Question) -> None:
        option_count = len(question.options)

        if option_count < self.POLL_OPTIONS_MIN:
            raise ValueError("Telegram poll requires at least 2 options")

        if option_count > self.POLL_OPTIONS_MAX:
            raise ValueError(
                f"Telegram poll supports at most {self.POLL_OPTIONS_MAX} options, got {option_count}"
            )

        for idx in question.right_answer_idx:
            if idx < 0 or idx >= option_count:
                raise ValueError(
                    f"right_answer_idx contains invalid index {idx} for {option_count} options"
                )

    def _can_send_as_single_poll(self, question: Question) -> bool:
        if question.image_code:
            return False

        poll_question = self._normalize_poll_question(question.question)

        if len(poll_question) > self.POLL_QUESTION_LIMIT:
            return False

        for option in question.options:
            normalized_option = option.strip()
            if not normalized_option:
                return False
            if len(normalized_option) > self.POLL_OPTION_LIMIT:
                return False

        explanation = self._normalize_quiz_explanation(question.explanation)
        if explanation is not None and len(explanation) > self.QUIZ_EXPLANATION_LIMIT:
            return False

        return True

    def _build_full_poll(self, question: Question) -> OutboundPollMessage:
        poll_question = self._normalize_poll_question(question.question)
        poll_options = [option.strip() for option in question.options]
        explanation = self._normalize_quiz_explanation(question.explanation)

        correct_option_id: int | None = None

        if len(question.right_answer_idx) == 1:
            correct_option_id = question.right_answer_idx[0]

        return OutboundPollMessage(
            question=poll_question,
            options=poll_options,
            correct_option_id=correct_option_id,
            explanation=explanation,
        )

    def _can_use_full_options_in_poll(self, question: Question) -> bool:
        for idx, option in enumerate(question.options):
            label = self._label_for_index(idx)
            text = f"{label}. {option.strip()}"

            if len(text) > self.POLL_OPTION_LIMIT:
                return False

        return True

    def _build_compact_poll(self, question: Question) -> OutboundPollMessage:
        poll_question = "Оберіть правильну відповідь 👇"

        if self._can_use_full_options_in_poll(question):
            poll_options = [
                #f"{self._label_for_index(i)}. {opt.strip()}"
                opt.strip()
                for i, opt in enumerate(question.options)
            ]
        else:
            poll_options = [
                self._label_for_index(i)
                for i in range(len(question.options))
            ]

        explanation = self._normalize_quiz_explanation(question.explanation)

        correct_option_id: int | None = None

        if len(question.right_answer_idx) == 1:
            correct_option_id = question.right_answer_idx[0]
        elif len(question.right_answer_idx) > 1:
            allows_multiple_answers = True

        return OutboundPollMessage(
            question=poll_question,
            options=poll_options,
            correct_option_id=correct_option_id,
            explanation=explanation,
        )

    def _build_content_message(self, question: Question, include_options_text: bool) -> OutboundMessage:
        base_text = self._build_base_text(question)
        options_text = self._build_options_text(question.options) if include_options_text else ''
        full_text = self._join_parts(base_text, options_text)

        if question.image_code:
            caption = self._fit_text(full_text, self.PHOTO_CAPTION_LIMIT)
            return OutboundPhotoMessage(
                photo_code=question.image_code,
                caption=caption,
            )

        text = self._fit_text(full_text, self.TEXT_LIMIT)
        return OutboundTextMessage(text=text)

    def _build_base_text(self, question: Question) -> str:
        parts: list[str] = []

        #section_name = question.section_name.strip()
        #if section_name:
        #    parts.append(f"Розділ: {section_name}")

        question_text = question.question.strip()
        if question_text:
            #parts.append(f"Питання:\n{question_text}")
            parts.append(f"<b>{question_text}</b>")

        return "\n\n".join(parts).strip()

    def _build_options_text(self, options: list[str]) -> str:
        lines = [" Варіанти відповіді:"]
        for idx, option in enumerate(options):
            label = self._label_for_index(idx)
            lines.append(f"<b>{label}</b>. {option.strip()}")
        return "\n".join(lines).strip()

    def _join_parts(self, *parts: str) -> str:
        clean_parts = [part.strip() for part in parts if part and part.strip()]
        return "\n\n".join(clean_parts)

    def _fit_text(self, text: str, limit: int) -> str:
        text = text.strip()
        if len(text) <= limit:
            return text

        cut = self._find_split_pos(text, limit - 1)
        trimmed = text[:cut].rstrip()

        if not trimmed:
            trimmed = text[: limit - 1].rstrip()

        return trimmed + "…"

    def _find_split_pos(self, text: str, limit: int) -> int:
        candidates = [
            text.rfind("\n\n", 0, limit + 1),
            text.rfind("\n", 0, limit + 1),
            text.rfind(" ", 0, limit + 1),
        ]
        best = max(candidates)
        if best > 0:
            return best
        return limit

    def _normalize_poll_question(self, text: str) -> str:
        text = " ".join(text.strip().split())
        if len(text) <= self.POLL_QUESTION_LIMIT:
            return text
        return text[: self.POLL_QUESTION_LIMIT - 1].rstrip() + "…"

    def _normalize_quiz_explanation(self, explanation: Optional[str]) -> Optional[str]:
        if not explanation:
            return None

        text = explanation.strip()

        lines = text.splitlines()
        if len(lines) > self.QUIZ_EXPLANATION_MAX_NEWLINES + 1:
            text = "\n".join(lines[: self.QUIZ_EXPLANATION_MAX_NEWLINES + 1])

        if len(text) <= self.QUIZ_EXPLANATION_LIMIT:
            return text

        return text[: self.QUIZ_EXPLANATION_LIMIT - 1].rstrip() + "…"

    def _label_for_index(self, idx: int) -> str:
        try:
            return self.OPTION_LABELS[idx]
        except IndexError as exc:
            raise ValueError(
                f"No label for option index {idx}; Telegram poll supports max {self.POLL_OPTIONS_MAX} options"
            ) from exc
