"""HTTP response helpers for AWS Lambda + API Gateway proxy integration."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

_CORS_HEADERS: Dict[str, str] = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,OPTIONS",
}


def _build(
    status_code: int,
    body: Any,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    headers = {**_CORS_HEADERS, "Content-Type": "application/json"}
    if extra_headers:
        headers.update(extra_headers)
    return {
        "statusCode": status_code,
        "headers": headers,
        "body": json.dumps(body),
    }


def ok(data: Any) -> Dict[str, Any]:
    """200 OK."""
    return _build(200, data)


def bad_request(message: str) -> Dict[str, Any]:
    """400 Bad Request."""
    return _build(400, {"error": message})


def not_found(message: str) -> Dict[str, Any]:
    """404 Not Found."""
    return _build(404, {"error": message})


def server_error(message: str = "Internal server error") -> Dict[str, Any]:
    """500 Internal Server Error."""
    return _build(500, {"error": message})
