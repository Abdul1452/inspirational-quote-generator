"""Tests for QuoteService."""

import pytest

from src.quotes.models import Quote
from src.quotes.service import QuoteNotFoundError, QuoteService

SAMPLE_QUOTES = [
    Quote(text="A wise quote.", author="Socrates", category="wisdom", tags=["philosophy"]),
    Quote(text="Be motivated!", author="Unknown", category="motivation", tags=["energy"]),
    Quote(
        text="Another wise quote.",
        author="Aristotle",
        category="wisdom",
        tags=["philosophy", "knowledge"],
    ),
    Quote(text="Stay happy.", author="Dalai Lama", category="happiness", tags=["joy"]),
    Quote(text="Be courageous.", author="Nelson Mandela", category="courage", tags=["bravery"]),
]


@pytest.fixture()
def service():
    return QuoteService(quotes=SAMPLE_QUOTES, seed=42)


# ── get_random ────────────────────────────────────────────────────────────────


def test_get_random_returns_quote(service):
    quote = service.get_random()
    assert isinstance(quote, Quote)
    assert quote in SAMPLE_QUOTES


def test_get_random_filter_by_category(service):
    quote = service.get_random(category="wisdom")
    assert quote.category == "wisdom"


def test_get_random_filter_by_category_case_insensitive(service):
    quote = service.get_random(category="WISDOM")
    assert quote.category == "wisdom"


def test_get_random_filter_by_author(service):
    quote = service.get_random(author="Socrates")
    assert "socrates" in quote.author.lower()


def test_get_random_filter_by_author_partial(service):
    quote = service.get_random(author="soc")
    assert "soc" in quote.author.lower()


def test_get_random_filter_by_tag(service):
    quote = service.get_random(tag="philosophy")
    assert "philosophy" in [t.lower() for t in quote.tags]


def test_get_random_combined_filters(service):
    quote = service.get_random(category="wisdom", tag="knowledge")
    assert quote.category == "wisdom"
    assert "knowledge" in [t.lower() for t in quote.tags]


def test_get_random_no_match_raises(service):
    with pytest.raises(QuoteNotFoundError):
        service.get_random(category="nonexistent")


def test_get_random_author_no_match_raises(service):
    with pytest.raises(QuoteNotFoundError):
        service.get_random(author="Julius Caesar")


def test_get_random_tag_no_match_raises(service):
    with pytest.raises(QuoteNotFoundError):
        service.get_random(tag="zzznomatch")


def test_get_random_is_deterministic_with_seed():
    svc1 = QuoteService(quotes=SAMPLE_QUOTES, seed=99)
    svc2 = QuoteService(quotes=SAMPLE_QUOTES, seed=99)
    results1 = [svc1.get_random() for _ in range(10)]
    results2 = [svc2.get_random() for _ in range(10)]
    assert results1 == results2


# ── list helpers ──────────────────────────────────────────────────────────────


def test_list_categories(service):
    cats = service.list_categories()
    assert sorted(cats) == cats  # must be sorted
    assert set(cats) == {"wisdom", "motivation", "happiness", "courage"}


def test_list_authors(service):
    authors = service.list_authors()
    assert sorted(authors) == authors
    assert "Socrates" in authors


def test_list_tags(service):
    tags = service.list_tags()
    assert sorted(tags) == tags
    assert "philosophy" in tags


# ── empty dataset edge case ───────────────────────────────────────────────────


def test_empty_dataset_raises():
    svc = QuoteService(quotes=[])
    with pytest.raises(QuoteNotFoundError):
        svc.get_random()
