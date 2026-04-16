# API Contract

## Base URL

```
https://<api-id>.execute-api.<region>.amazonaws.com/<stage>
```

Replace `<api-id>`, `<region>`, and `<stage>` with the values from the CloudFormation output after deployment.

---

## Endpoints

### `GET /health`

Liveness check.

**Response 200**
```json
{ "status": "ok" }
```

---

### `GET /quote`

Returns a single random inspirational quote. Optionally filter results.

**Query parameters**

| Parameter  | Type   | Required | Description                                     |
|------------|--------|----------|-------------------------------------------------|
| `category` | string | No       | Case-insensitive category name (e.g. `wisdom`)  |
| `author`   | string | No       | Case-insensitive partial or full author name    |
| `tag`      | string | No       | Case-insensitive tag name (e.g. `perseverance`) |

**Response 200**
```json
{
  "text":     "The only way to do great work is to love what you do.",
  "author":   "Steve Jobs",
  "category": "motivation",
  "tags":     ["work", "passion"],
  "source":   null
}
```

**Response 400** – unknown category
```json
{ "error": "Unknown category 'xyz'. Available: courage, creativity, ..." }
```

**Response 404** – no quotes match filters
```json
{ "error": "No quotes found matching {author='Julius Caesar'}." }
```

---

### `GET /quote/categories`

Lists all available quote categories.

**Response 200**
```json
{ "categories": ["courage", "creativity", "happiness", "leadership", "mindfulness", "motivation", "perseverance", "wisdom"] }
```

---

### `GET /quote/authors`

Lists all available authors.

**Response 200**
```json
{ "authors": ["Albert Einstein", "Aristotle", "Benjamin Franklin", "..."] }
```

---

### `GET /quote/tags`

Lists all available tags.

**Response 200**
```json
{ "tags": ["abundance", "action", "art", "authenticity", "..."] }
```

---

## CORS

All responses include:

```
Access-Control-Allow-Origin:  *
Access-Control-Allow-Headers: Content-Type
Access-Control-Allow-Methods: GET,OPTIONS
```

---

## Scheduled Delivery (EventBridge)

A second Lambda function (`quote-generator-scheduler-<stage>`) runs daily at 08:00 UTC by default.  
It logs a structured JSON entry to CloudWatch:

```json
{
  "timestamp":      "2026-01-01T08:00:01Z",
  "level":          "INFO",
  "logger":         "src.handlers.scheduler",
  "message":        "Daily inspirational quote",
  "quote_text":     "Fall seven times, stand up eight.",
  "quote_author":   "Japanese Proverb",
  "quote_category": "perseverance",
  "quote_tags":     ["resilience", "recovery"]
}
```

The schedule expression is configurable via the `ScheduleExpression` SAM parameter.
