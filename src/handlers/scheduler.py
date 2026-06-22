"""AWS Lambda handler for the EventBridge scheduled rule.

Generates a random inspirational quote, logs it as a structured CloudWatch log
entry, and delivers it to an incoming webhook (Slack/Discord) when one is
configured via ``NOTIFY_WEBHOOK_URL``.
"""

from __future__ import annotations

import time
from typing import Any, Dict

from src.quotes.service import QuoteService
from src.utils.logger import get_logger
from src.utils.notifier import send_quote_notification

logger = get_logger(__name__)

_service = QuoteService()


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """EventBridge scheduled rule entry point."""
    start = time.perf_counter()

    source = event.get("source", "aws.events")
    detail_type = event.get("detail-type", "Scheduled Event")

    logger.info("Scheduled event received", source=source, detail_type=detail_type)

    quote = _service.get_random()

    logger.info(
        "Daily inspirational quote",
        quote_text=quote.text,
        quote_author=quote.author,
        quote_category=quote.category,
        quote_tags=quote.tags,
    )

    delivered = send_quote_notification(quote)

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info("Scheduler run complete", delivered=delivered, elapsed_ms=elapsed_ms)

    return {
        "statusCode": 200,
        "quote": quote.to_dict(),
        "notified": delivered,
    }
