"""Tests for the EventBridge scheduler Lambda handler."""

from src.handlers.scheduler import handler


def _scheduled_event():
    return {
        "version": "0",
        "id": "test-event-id",
        "source": "aws.events",
        "account": "123456789012",
        "time": "2026-01-01T08:00:00Z",
        "region": "us-east-1",
        "detail-type": "Scheduled Event",
        "detail": {},
    }


def test_scheduler_returns_200():
    result = handler(_scheduled_event(), context=None)
    assert result["statusCode"] == 200


def test_scheduler_returns_quote():
    result = handler(_scheduled_event(), context=None)
    quote = result["quote"]
    assert "text" in quote
    assert "author" in quote
    assert "category" in quote


def test_scheduler_quote_in_known_dataset():
    from src.quotes.data import QUOTES

    result = handler(_scheduled_event(), context=None)
    texts = {q.text for q in QUOTES}
    assert result["quote"]["text"] in texts


def test_scheduler_is_callable_multiple_times():
    for _ in range(5):
        result = handler(_scheduled_event(), context=None)
        assert result["statusCode"] == 200
