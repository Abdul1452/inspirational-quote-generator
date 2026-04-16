"""AWS Lambda handler for API Gateway proxy events.

Routes:
  GET /quote            – random quote (optional ?category, ?author, ?tag filters)
  GET /quote/categories – list all categories
  GET /quote/authors    – list all authors
  GET /quote/tags       – list all tags
  GET /health           – liveness check
"""

from __future__ import annotations

import time
from typing import Any, Dict

from src.quotes.service import QuoteNotFoundError, QuoteService
from src.utils.logger import get_logger
from src.utils.response import bad_request, not_found, ok, server_error

logger = get_logger(__name__)

_service = QuoteService()


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Main Lambda entry point for API Gateway proxy integration."""
    start = time.perf_counter()

    method = event.get("httpMethod", "GET")
    path = (event.get("path") or "/").rstrip("/") or "/"
    params = event.get("queryStringParameters") or {}

    logger.info("Request received", method=method, path=path, params=params)

    try:
        response = _route(method, path, params)
    except Exception as exc:  # noqa: BLE001
        logger.error("Unhandled exception", error=str(exc))
        response = server_error()

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info(
        "Request completed",
        status_code=response["statusCode"],
        elapsed_ms=elapsed_ms,
    )
    return response


def _route(method: str, path: str, params: Dict[str, str]) -> Dict[str, Any]:
    if method == "OPTIONS":
        return ok({})

    if method != "GET":
        return bad_request(f"Method {method} not allowed.")

    if path == "/health":
        return ok({"status": "ok"})

    if path == "/quote/categories":
        return ok({"categories": _service.list_categories()})

    if path == "/quote/authors":
        return ok({"authors": _service.list_authors()})

    if path == "/quote/tags":
        return ok({"tags": _service.list_tags()})

    if path == "/quote":
        return _handle_random_quote(params)

    return not_found(f"Unknown path: {path}")


def _handle_random_quote(params: Dict[str, str]) -> Dict[str, Any]:
    category = params.get("category") or None
    author = params.get("author") or None
    tag = params.get("tag") or None

    # Validate category if provided
    if category and category.lower() not in [c.lower() for c in _service.list_categories()]:
        return bad_request(
            f"Unknown category '{category}'. "
            f"Available: {', '.join(_service.list_categories())}."
        )

    try:
        quote = _service.get_random(category=category, author=author, tag=tag)
    except QuoteNotFoundError as exc:
        return not_found(str(exc))

    return ok(quote.to_dict())
