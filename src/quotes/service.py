"""Quote retrieval and filtering service."""

from __future__ import annotations

import random
from typing import List, Optional

from src.quotes.data import QUOTES
from src.quotes.models import Quote


class QuoteNotFoundError(Exception):
    """Raised when no quotes match the requested filters."""


class QuoteService:
    """Provides quote retrieval with optional filtering."""

    def __init__(self, quotes: Optional[List[Quote]] = None, seed: Optional[int] = None) -> None:
        self._quotes: List[Quote] = list(quotes if quotes is not None else QUOTES)
        self._rng = random.Random(seed)

    # ── public API ─────────────────────────────────────────────────────────────

    def get_random(
        self,
        category: Optional[str] = None,
        author: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> Quote:
        """Return a single random quote, optionally filtered.

        Args:
            category: Case-insensitive category name (e.g. ``"wisdom"``).
            author:   Case-insensitive partial or full author name.
            tag:      Case-insensitive tag to filter by.

        Raises:
            QuoteNotFoundError: When no quotes match the given filters.

        Returns:
            A randomly selected :class:`Quote`.
        """
        pool = self._filter(category=category, author=author, tag=tag)
        if not pool:
            criteria = self._format_criteria(category=category, author=author, tag=tag)
            raise QuoteNotFoundError(f"No quotes found matching {criteria}.")
        return self._rng.choice(pool)

    def list_categories(self) -> List[str]:
        """Return sorted list of unique categories."""
        return sorted({q.category for q in self._quotes})

    def list_authors(self) -> List[str]:
        """Return sorted list of unique authors."""
        return sorted({q.author for q in self._quotes})

    def list_tags(self) -> List[str]:
        """Return sorted list of unique tags."""
        return sorted({tag for q in self._quotes for tag in q.tags})

    # ── private helpers ────────────────────────────────────────────────────────

    def _filter(
        self,
        category: Optional[str],
        author: Optional[str],
        tag: Optional[str],
    ) -> List[Quote]:
        pool = self._quotes
        if category:
            pool = [q for q in pool if q.category.lower() == category.lower()]
        if author:
            pool = [q for q in pool if author.lower() in q.author.lower()]
        if tag:
            pool = [q for q in pool if any(tag.lower() == t.lower() for t in q.tags)]
        return pool

    @staticmethod
    def _format_criteria(**kwargs: Optional[str]) -> str:
        parts = [f"{k}={v!r}" for k, v in kwargs.items() if v is not None]
        return "{" + ", ".join(parts) + "}" if parts else "{}"
