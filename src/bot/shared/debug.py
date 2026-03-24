import time
from logging import Logger, getLogger


class track_time:
    def __init__(self, name: str, logger: Logger | None = None):
        self._name = name
        self._logger = logger or getLogger('track_time')

    def __enter__(self):
        self.start_time = time.time()  # Start time
        return self  # Return self for potential use within the block

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.time()    # End time
        execution_time = self.end_time - self.start_time
        self._logger.info(f"{self._name}: {execution_time:.8f} seconds")
