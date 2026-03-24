from typing import Optional, Literal, Any
from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class OutboundTextMessage:
    kind: Literal["text"] = "text"
    text: str = ""
    keyboard: Any = None


@dataclass(slots=True, frozen=True)
class OutboundPhotoMessage:
    kind: Literal["photo"] = "photo"
    photo_code: str = ""
    caption: Optional[str] = None
    keyboard: Any = None


@dataclass(slots=True, frozen=True)
class OutboundPollMessage:
    kind: Literal["poll"] = "poll"
    question: str = ""
    options: list[str] = field(default_factory=list)
    correct_option_id: Optional[int] = None
    explanation: Optional[str] = None


OutboundMessage = OutboundTextMessage | OutboundPhotoMessage | OutboundPollMessage