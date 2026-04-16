"""Static quote dataset bundled with the application."""

from __future__ import annotations

from src.quotes.models import Quote

QUOTES: list[Quote] = [
    # ── Motivation ─────────────────────────────────────────────────────────────
    Quote(
        text="The only way to do great work is to love what you do.",
        author="Steve Jobs",
        category="motivation",
        tags=["work", "passion"],
    ),
    Quote(
        text="It does not matter how slowly you go as long as you do not stop.",
        author="Confucius",
        category="motivation",
        tags=["perseverance", "progress"],
    ),
    Quote(
        text=(
            "Success is not final, failure is not fatal:"
            " it is the courage to continue that counts."
        ),
        author="Winston Churchill",
        category="motivation",
        tags=["success", "failure", "courage"],
    ),
    Quote(
        text="Believe you can and you're halfway there.",
        author="Theodore Roosevelt",
        category="motivation",
        tags=["belief", "confidence"],
    ),
    Quote(
        text="Don't watch the clock; do what it does. Keep going.",
        author="Sam Levenson",
        category="motivation",
        tags=["time", "perseverance"],
    ),
    Quote(
        text="Your time is limited, so don't waste it living someone else's life.",
        author="Steve Jobs",
        category="motivation",
        tags=["time", "authenticity"],
    ),
    Quote(
        text="The future belongs to those who believe in the beauty of their dreams.",
        author="Eleanor Roosevelt",
        category="motivation",
        tags=["future", "dreams"],
    ),
    Quote(
        text="It always seems impossible until it's done.",
        author="Nelson Mandela",
        category="motivation",
        tags=["perseverance", "achievement"],
    ),
    # ── Wisdom ─────────────────────────────────────────────────────────────────
    Quote(
        text="The unexamined life is not worth living.",
        author="Socrates",
        category="wisdom",
        tags=["reflection", "philosophy"],
    ),
    Quote(
        text="In the middle of every difficulty lies opportunity.",
        author="Albert Einstein",
        category="wisdom",
        tags=["difficulty", "opportunity"],
    ),
    Quote(
        text="Knowing yourself is the beginning of all wisdom.",
        author="Aristotle",
        category="wisdom",
        tags=["self-knowledge", "philosophy"],
    ),
    Quote(
        text="Life is what happens when you're busy making other plans.",
        author="John Lennon",
        category="wisdom",
        tags=["life", "planning"],
    ),
    Quote(
        text="The measure of intelligence is the ability to change.",
        author="Albert Einstein",
        category="wisdom",
        tags=["intelligence", "change"],
    ),
    Quote(
        text="Turn your wounds into wisdom.",
        author="Oprah Winfrey",
        category="wisdom",
        tags=["growth", "resilience"],
    ),
    # ── Courage ────────────────────────────────────────────────────────────────
    Quote(
        text="Courage is not the absence of fear, but the triumph over it.",
        author="Nelson Mandela",
        category="courage",
        tags=["fear", "bravery"],
    ),
    Quote(
        text=(
            "You gain strength, courage and confidence by every experience"
            " in which you really stop to look fear in the face."
        ),
        author="Eleanor Roosevelt",
        category="courage",
        tags=["fear", "confidence", "strength"],
    ),
    Quote(
        text="It takes courage to grow up and become who you really are.",
        author="E. E. Cummings",
        category="courage",
        tags=["growth", "authenticity"],
    ),
    Quote(
        text="Fortune favors the bold.",
        author="Virgil",
        category="courage",
        tags=["boldness", "risk"],
    ),
    # ── Happiness ──────────────────────────────────────────────────────────────
    Quote(
        text="Happiness is not something ready-made. It comes from your own actions.",
        author="Dalai Lama",
        category="happiness",
        tags=["action", "joy"],
    ),
    Quote(
        text="The purpose of our lives is to be happy.",
        author="Dalai Lama",
        category="happiness",
        tags=["purpose", "joy"],
    ),
    Quote(
        text="Happiness is when what you think, what you say, and what you do are in harmony.",
        author="Mahatma Gandhi",
        category="happiness",
        tags=["harmony", "integrity"],
    ),
    Quote(
        text="Count your age by friends, not years. Count your life by smiles, not tears.",
        author="John Lennon",
        category="happiness",
        tags=["friendship", "gratitude"],
    ),
    # ── Leadership ─────────────────────────────────────────────────────────────
    Quote(
        text="A leader is one who knows the way, goes the way, and shows the way.",
        author="John C. Maxwell",
        category="leadership",
        tags=["example", "direction"],
    ),
    Quote(
        text="Leadership and learning are indispensable to each other.",
        author="John F. Kennedy",
        category="leadership",
        tags=["learning", "growth"],
    ),
    Quote(
        text="The greatest leader is not necessarily the one who does the greatest things. "
        "He is the one that gets the people to do the greatest things.",
        author="Ronald Reagan",
        category="leadership",
        tags=["teamwork", "influence"],
    ),
    # ── Perseverance ───────────────────────────────────────────────────────────
    Quote(
        text="Fall seven times, stand up eight.",
        author="Japanese Proverb",
        category="perseverance",
        tags=["resilience", "recovery"],
    ),
    Quote(
        text="Our greatest glory is not in never falling but in rising every time we fall.",
        author="Confucius",
        category="perseverance",
        tags=["resilience", "glory"],
    ),
    Quote(
        text="Energy and persistence conquer all things.",
        author="Benjamin Franklin",
        category="perseverance",
        tags=["energy", "persistence"],
    ),
    # ── Creativity ─────────────────────────────────────────────────────────────
    Quote(
        text="Creativity is intelligence having fun.",
        author="Albert Einstein",
        category="creativity",
        tags=["intelligence", "play"],
    ),
    Quote(
        text="You can't use up creativity. The more you use, the more you have.",
        author="Maya Angelou",
        category="creativity",
        tags=["abundance", "art"],
    ),
    Quote(
        text="The desire to create is one of the deepest yearnings of the human soul.",
        author="Dieter F. Uchtdorf",
        category="creativity",
        tags=["soul", "purpose"],
    ),
    # ── Mindfulness ────────────────────────────────────────────────────────────
    Quote(
        text="Be present in all things and thankful for all things.",
        author="Maya Angelou",
        category="mindfulness",
        tags=["gratitude", "presence"],
    ),
    Quote(
        text=(
            "Do not dwell in the past, do not dream of the future,"
            " concentrate the mind on the present moment."
        ),
        author="Buddha",
        category="mindfulness",
        tags=["present", "focus"],
    ),
    Quote(
        text="Almost everything will work again if you unplug it for a few minutes, including you.",
        author="Anne Lamott",
        category="mindfulness",
        tags=["rest", "reset"],
    ),
]
