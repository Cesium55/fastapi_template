import asyncio
import logging
from pathlib import Path
from typing import AsyncGenerator, Generator

from basic_utils.config import settings


LOGS_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_FILE = LOGS_DIR / "app.log"


def _configure_logger(name: str) -> logging.Logger:
    """
    Создает и настраивает стандартный logger.

    Повторная настройка одного и того же logger не выполняется, чтобы
    не дублировать handlers при множественных вызовах.
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level.upper())
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter(settings.log_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger


class SyncLogger:
    """Синхронная обертка над стандартным logging.Logger."""

    def __init__(self, name: str) -> None:
        self._logger = _configure_logger(name)

    def debug(self, message: str, *args, **kwargs) -> None:
        self._logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs) -> None:
        self._logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs) -> None:
        self._logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        self._logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs) -> None:
        self._logger.critical(message, *args, **kwargs)

    def exception(self, message: str, *args, **kwargs) -> None:
        self._logger.exception(message, *args, **kwargs)


class AsyncLogger:
    """Асинхронная обертка над стандартным logging.Logger."""

    def __init__(self, name: str) -> None:
        self._logger = _configure_logger(name)

    async def debug(self, message: str, *args, **kwargs) -> None:
        await asyncio.to_thread(self._logger.debug, message, *args, **kwargs)

    async def info(self, message: str, *args, **kwargs) -> None:
        await asyncio.to_thread(self._logger.info, message, *args, **kwargs)

    async def warning(self, message: str, *args, **kwargs) -> None:
        await asyncio.to_thread(self._logger.warning, message, *args, **kwargs)

    async def error(self, message: str, *args, **kwargs) -> None:
        await asyncio.to_thread(self._logger.error, message, *args, **kwargs)

    async def critical(self, message: str, *args, **kwargs) -> None:
        await asyncio.to_thread(self._logger.critical, message, *args, **kwargs)

    async def exception(self, message: str, *args, **kwargs) -> None:
        await asyncio.to_thread(self._logger.exception, message, *args, **kwargs)


def get_sync_logger(name: str = "app") -> SyncLogger:
    """Возвращает синхронный logger."""
    return SyncLogger(name)


def get_logger(name: str = "app") -> AsyncLogger:
    """Возвращает асинхронный logger."""
    return AsyncLogger(name)


def get_sync_logger_generator(name: str = "app") -> Generator[SyncLogger, None, None]:
    """Синхронный генератор logger для dependency injection."""
    yield get_sync_logger(name)


async def get_async_logger_generator(
    name: str = "app",
) -> AsyncGenerator[AsyncLogger, None]:
    """Асинхронный генератор logger для dependency injection."""
    yield get_logger(name)
