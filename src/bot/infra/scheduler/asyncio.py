import asyncio
import logging
import random
from datetime import datetime, timedelta, time
from bot.application.usecases import SendQuestionToChatUseCase


class AsyncioScheduler:
    def __init__(self, send_uc: SendQuestionToChatUseCase):
        self._send_uc = send_uc
        self._logger = logging.getLogger(__name__)

    async def start(self):
        await asyncio.gather(
            self._daily_sends_loop()
        )

    async def _tick(self):
        await self._send_uc.execute()
    
    async def _daily_sends_loop(self):
        while True:
            now = datetime.now()
            target = datetime.combine(now.date(), time(17, 0))

            if now >= target:
                target += timedelta(days=1)

            sleep_seconds = (target - now).total_seconds()
            self._logger.debug("_daily_sends_loop: next run at %s (%f)", target.isoformat(), sleep_seconds)
            await asyncio.sleep(sleep_seconds)

            await self._sends_loop()
    
    async def _sends_loop(self):
        for _ in range(random.randint(5,7)):

            sleep_seconds = random.randrange(120, 600)
            await asyncio.sleep(sleep_seconds)

            await self._send_uc.execute()

