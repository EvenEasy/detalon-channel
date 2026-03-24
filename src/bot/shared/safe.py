import asyncio
import signal
import sys
from logging import Logger
from typing import Optional, Any, Callable, TypeVar, Awaitable


T = TypeVar("T")


def safe_execute(call: Callable[..., T],
                 *args,
                 _default: Any = None,
                 _exceptions = Exception,
                 _logger: Optional[Logger] = None,
                 **kwargs
) -> tuple[bool, T | None]:
    """
    Execute a func without break system
    """
    try:
        return True, call(*args, **kwargs)
    except _exceptions as e:
        if _logger:
            _logger.warning(f"Ignored {call.__qualname__}: {e}")
        return False, _default

async def safe_execute_coro(coro: Awaitable[T],
                            default: Any = None,
                            exceptions = Exception,
                            logger: Optional[Logger] = None
) -> tuple[bool, T | None]:
    try:
        return True, await coro
    except exceptions as e:
        if logger:
            logger.warning(f"Ignored {coro.__qualname__}: {e}")
        return False, default

async def safe_execute_gather(*coro, logger: Optional[Logger] = None):
    try:
        async with asyncio.TaskGroup() as tg:
            for task in coro:
                tg.create_task(safe_execute_coro(task, logger=logger))
                if logger: logger.warning("task %s created", task.__qualname__)
    except KeyboardInterrupt:
        return

def signal_handler():
    print("Program terminated.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
