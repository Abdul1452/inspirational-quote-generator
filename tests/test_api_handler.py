"""Tests for the API Gateway Lambda handler."""

import json

from src.handlers.api import handler


def _call(path, params=None, method="GET"):
    event = {
        "httpMethod": method,
        "path": path,
        "queryStringParameters": params or {},
    }
    return handler(event, context=None)


# ── /health ───────────────────────────────────────────────────────────────────


def test_health_returns_200():
    resp = _call("/health")
    assert resp["statusCode"] == 200
    body = json.loads(resp["body"])
    assert body["status"] == "ok"


# ── /quote ────────────────────────────────────────────────────────────────────


def test_random_quote_returns_200():
    resp = _call("/quote")
    assert resp["statusCode"] == 200
    body = json.loads(resp["body"])
    assert "text" in body
    assert "author" in body
    assert "category" in body


def test_random_quote_filter_by_category():
    resp = _call("/quote", params={"category": "wisdom"})
    assert resp["statusCode"] == 200
    body = json.loads(resp["body"])
    assert body["category"] == "wisdom"


def test_random_quote_invalid_category_returns_400():
    resp = _call("/quote", params={"category": "totally_fake_category"})
    assert resp["statusCode"] == 400
    body = json.loads(resp["body"])
    assert "error" in body


def test_random_quote_author_filter():
    resp = _call("/quote", params={"author": "Einstein"})
    assert resp["statusCode"] in (200, 404)


def test_random_quote_author_no_match_returns_404():
    resp = _call("/quote", params={"author": "zzznobody_ever_zzz"})
    assert resp["statusCode"] == 404


def test_random_quote_tag_filter():
    resp = _call("/quote", params={"tag": "philosophy"})
    assert resp["statusCode"] == 200


def test_random_quote_tag_no_match_returns_404():
    resp = _call("/quote", params={"tag": "zzznomatch"})
    assert resp["statusCode"] == 404


# ── /quote/categories ─────────────────────────────────────────────────────────


def test_categories_returns_list():
    resp = _call("/quote/categories")
    assert resp["statusCode"] == 200
    body = json.loads(resp["body"])
    assert isinstance(body["categories"], list)
    assert len(body["categories"]) > 0


# ── /quote/authors ────────────────────────────────────────────────────────────


def test_authors_returns_list():
    resp = _call("/quote/authors")
    assert resp["statusCode"] == 200
    body = json.loads(resp["body"])
    assert isinstance(body["authors"], list)


# ── /quote/tags ───────────────────────────────────────────────────────────────


def test_tags_returns_list():
    resp = _call("/quote/tags")
    assert resp["statusCode"] == 200
    body = json.loads(resp["body"])
    assert isinstance(body["tags"], list)


# ── CORS headers ──────────────────────────────────────────────────────────────


def test_cors_headers_present():
    resp = _call("/quote")
    assert "Access-Control-Allow-Origin" in resp["headers"]
    assert resp["headers"]["Access-Control-Allow-Origin"] == "*"


def test_options_returns_200():
    resp = _call("/quote", method="OPTIONS")
    assert resp["statusCode"] == 200


# ── unknown paths & methods ───────────────────────────────────────────────────


def test_unknown_path_returns_404():
    resp = _call("/unknown/path")
    assert resp["statusCode"] == 404


def test_post_returns_400():
    resp = _call("/quote", method="POST")
    assert resp["statusCode"] == 400


# ── trailing slash normalisation ─────────────────────────────────────────────


def test_health_with_trailing_slash():
    resp = _call("/health/")
    assert resp["statusCode"] == 200
