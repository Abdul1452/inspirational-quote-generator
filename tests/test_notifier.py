"""Tests for the webhook notifier."""

import urllib.error
from unittest.mock import patch

from src.quotes.models import Quote
from src.utils.notifier import format_message, send_quote_notification

_QUOTE = Quote(
    text="Stay hungry, stay foolish.",
    author="Steve Jobs",
    category="wisdom",
    tags=["motivation"],
)


class _FakeResponse:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def getcode(self):
        return self.status


def test_format_message_contains_text_and_author():
    message = format_message(_QUOTE)
    assert "Stay hungry, stay foolish." in message
    assert "Steve Jobs" in message


def test_returns_false_when_no_url(monkeypatch):
    monkeypatch.delenv("NOTIFY_WEBHOOK_URL", raising=False)
    assert send_quote_notification(_QUOTE) is False


def test_posts_to_webhook_and_returns_true():
    with patch("urllib.request.urlopen", return_value=_FakeResponse()) as mock_open:
        ok = send_quote_notification(_QUOTE, webhook_url="https://example.com/hook")
    assert ok is True
    assert mock_open.called
    request = mock_open.call_args[0][0]
    assert request.method == "POST"
    body = request.data.decode("utf-8")
    assert "Steve Jobs" in body
    assert "Stay hungry" in body


def test_uses_env_var_when_url_not_passed(monkeypatch):
    monkeypatch.setenv("NOTIFY_WEBHOOK_URL", "https://example.com/from-env")
    with patch("urllib.request.urlopen", return_value=_FakeResponse()) as mock_open:
        assert send_quote_notification(_QUOTE) is True
    assert mock_open.call_args[0][0].full_url == "https://example.com/from-env"


def test_returns_false_on_network_error():
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("boom")):
        assert send_quote_notification(_QUOTE, webhook_url="https://example.com/hook") is False


def test_returns_false_on_non_2xx():
    class _ErrorResponse(_FakeResponse):
        status = 500

    with patch("urllib.request.urlopen", return_value=_ErrorResponse()):
        assert send_quote_notification(_QUOTE, webhook_url="https://example.com/hook") is False
