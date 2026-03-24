from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

    service_name: str = Field(default="detalon-channel")
    log_level: str = Field(default="INFO", pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")

    admin_id: int = Field(..., description="Root admin telegram id")
    bot_token: str = Field(..., description="Telegram bot token")
    channel_id: int = Field(..., description="Telegram channel ID")
    questions_path_json: str = Field(..., description="Paht to JSON file with questions")
    image_provider_url: str = Field(...)

    @validator("channel_id", "bot_token", pre=True)
    def validate_not_empty(cls, v):
        if not v:
            raise ValueError("Cannot be empty")
        return v


def load_config() -> AppSettings:
    return AppSettings()  # type: ignore