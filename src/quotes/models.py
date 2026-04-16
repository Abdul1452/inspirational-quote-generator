"""Quote domain model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class Quote:
    """Immutable representation of a single inspirational quote."""

    text: str
    author: str
    category: str
    tags: List[str] = field(default_factory=list)
    source: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "author": self.author,
            "category": self.category,
            "tags": list(self.tags),
            "source": self.source,
        }
