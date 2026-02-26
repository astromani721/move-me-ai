"""Structured JSON logging configuration."""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone

_SKIP_ATTRS = frozenset(
    {
        "name", "msg", "args", "levelname", "levelno", "pathname",
        "filename", "module", "exc_info", "exc_text", "stack_info",
        "lineno", "funcName", "created", "msecs", "relativeCreated",
        "thread", "threadName", "processName", "process", "message",
        "taskName",
    }
)


class StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        entry: dict[str, object] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            entry["exc"] = self.formatException(record.exc_info)
        for key, val in record.__dict__.items():
            if key not in _SKIP_ATTRS:
                entry[key] = val
        return json.dumps(entry)


def configure_logging(level: str = "INFO") -> None:
    """Configure root logger with structured JSON output to stderr."""
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(StructuredFormatter())
    root = logging.getLogger()
    root.setLevel(level.upper())
    root.handlers = [handler]
