"""Tests for Quote domain model."""

import pytest

from src.quotes.models import Quote


def test_quote_to_dict_basic():
    q = Quote(text="Test quote.", author="Author A", category="wisdom")
    d = q.to_dict()
    assert d["text"] == "Test quote."
    assert d["author"] == "Author A"
    assert d["category"] == "wisdom"
    assert d["tags"] == []
    assert d["source"] is None


def test_quote_to_dict_with_tags_and_source():
    q = Quote(
        text="Another quote.",
        author="Author B",
        category="motivation",
        tags=["hope", "future"],
        source="Book Title",
    )
    d = q.to_dict()
    assert d["tags"] == ["hope", "future"]
    assert d["source"] == "Book Title"


def test_quote_is_immutable():
    q = Quote(text="X", author="Y", category="z")
    with pytest.raises(AttributeError):
        q.text = "modified"  # type: ignore[misc]


def test_quote_tags_default_is_independent():
    q1 = Quote(text="A", author="B", category="c")
    q2 = Quote(text="D", author="E", category="f")
    assert q1.tags is not q2.tags
