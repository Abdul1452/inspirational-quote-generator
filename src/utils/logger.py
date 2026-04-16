"""Structured logging utility."""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any, Optional


def _get_level() -> int:
    return getattr(logging, os.environ.get("LOG_LEVEL", "INFO").upper(), logging.INFO)


logging.basicConfig(
    format="%(message)s",
    level=_get_level(),
)


class StructuredLogger:
    """Emits JSON-formatted log lines compatible with CloudWatch Logs Insights."""

    def __init__(self, name: str) -> None:
        self._logger = logging.getLogger(name)
        self._logger.setLevel(_get_level())

    def _emit(self, level: str, message: str, **extra: Any) -> None:
        record: dict[str, Any] = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "level": level,
            "logger": self._logger.name,
            "message": message,
        }
        record.update(extra)
        self._logger.log(getattr(logging, level), json.dumps(record))

    def info(self, message: str, **extra: Any) -> None:
        self._emit("INFO", message, **extra)

    def warning(self, message: str, **extra: Any) -> None:
        self._emit("WARNING", message, **extra)

    def error(self, message: str, **extra: Any) -> None:
        self._emit("ERROR", message, **extra)

    def debug(self, message: str, **extra: Any) -> None:
        self._emit("DEBUG", message, **extra)


def get_logger(name: Optional[str] = None) -> StructuredLogger:
    return StructuredLogger(name or __name__)
