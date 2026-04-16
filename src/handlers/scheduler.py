"""AWS Lambda handler for EventBridge scheduled rule.

Generates a random inspirational quote and logs it as a structured CloudWatch
log entry.  Can be extended to deliver via SNS, SES, Slack, etc.
"""

from __future__ import annotations

import time
from typing import Any, Dict

from src.quotes.service import QuoteService
from src.utils.logger import get_logger

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

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info("Scheduler run complete", elapsed_ms=elapsed_ms)

    return {
        "statusCode": 200,
        "quote": quote.to_dict(),
    }
