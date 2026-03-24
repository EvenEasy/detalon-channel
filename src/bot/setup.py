import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d %(funcName)s() - %(message)s",
        stream=sys.stdout,
    )
