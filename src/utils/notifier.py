"""Outbound notification delivery for the daily quote.

Posts a formatted quote to an incoming webhook (Slack- or Discord-compatible)
using only the Python standard library. Delivery is best-effort: any failure is
logged and swallowed so the scheduled Lambda never fails because of it.

Configure the target with the ``NOTIFY_WEBHOOK_URL`` environment variable. When
it is unset the notifier is a no-op and the caller still logs the quote.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Optional

from src.quotes.models import Quote
from src.utils.logger import get_logger

logger = get_logger(__name__)

_TIMEOUT_SECONDS = 5


def format_message(quote: Quote) -> str:
    """Render a quote as a human-friendly notification string."""
    return f'\U0001f4a1 Daily inspiration\n\n"{quote.text}"\n— {quote.author}'


def send_quote_notification(quote: Quote, webhook_url: Optional[str] = None) -> bool:
    """Post the quote to an incoming webhook.

    Args:
        quote: The quote to deliver.
        webhook_url: Target webhook URL. Falls back to the ``NOTIFY_WEBHOOK_URL``
            environment variable when not provided.

    Returns:
        ``True`` when the webhook accepts the request, ``False`` otherwise
        (including when no webhook URL is configured).
    """
    url = (webhook_url or os.environ.get("NOTIFY_WEBHOOK_URL", "")).strip()
    if not url:
        logger.info("Notification skipped: NOTIFY_WEBHOOK_URL not set")
        return False

    message = format_message(quote)
    # "text" satisfies Slack; "content" satisfies Discord. Each ignores the other.
    payload = json.dumps({"text": message, "content": message}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=_TIMEOUT_SECONDS) as response:
            status = getattr(response, "status", None) or response.getcode()
        if 200 <= status < 300:
            logger.info("Notification delivered", status=status)
            return True
        logger.warning("Notification rejected", status=status)
        return False
    except urllib.error.URLError as exc:
        logger.error("Notification failed", error=str(exc))
        return False
    except Exception as exc:  # defensive: never let delivery crash the Lambda
        logger.error("Notification error", error=str(exc))
        return False
