import sys

from loguru import logger

from core.config import settings


logger.remove(0)

logger.add(
    sys.stderr,
    level=settings.LOG_LEVEL,
    enqueue=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
    colorize=True,
)

__all__ = ["logger"]
