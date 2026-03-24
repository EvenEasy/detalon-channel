import asyncio
from bot.config import load_config
from bot.infra.delivery import TelegramDelivery
from bot.infra.scheduler import AsyncioScheduler
from bot.infra.questionnaire import JsonQuestionnaireProvider
from bot.application.usecases import SendQuestionToChatUseCase
from .setup import setup_logging


async def main():
    settings = load_config()
    setup_logging(settings.log_level)

    # Load questionnnaires storage
    questionnaire = JsonQuestionnaireProvider(settings.questions_path_json, settings.image_provider_url)
    delivery = TelegramDelivery(settings.bot_token, settings.channel_id)
    
    # Use cases
    send_question_uc = SendQuestionToChatUseCase(delivery, questionnaire)
    scheduler = AsyncioScheduler(send_question_uc)

    # Test
    await scheduler.start()

if __name__ == '__main__':
    asyncio.run(main())