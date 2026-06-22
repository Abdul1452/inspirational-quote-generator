# Inspirational Quote Generator

A serverless application that delivers random inspirational quotes via a REST API and a daily scheduled notification — pushed to a Slack or Discord webhook — running on AWS Lambda.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                          AWS Cloud                           │
│                                                              │
│  API Gateway ──► QuoteApiFunction (Lambda)                   │
│                       └─ src/handlers/api.py                 │
│                                                              │
│  EventBridge (daily 08:00 UTC)                               │
│      └──► QuoteSchedulerFunction (Lambda)                    │
│                └─ src/handlers/scheduler.py                  │
│                                                              │
│  Both functions log structured JSON to CloudWatch Logs       │
└──────────────────────────────────────────────────────────────┘

Core domain (no external dependencies):
  src/quotes/models.py   – Quote dataclass
  src/quotes/data.py     – 30+ bundled quotes across 8 categories
  src/quotes/service.py  – QuoteService (random selection + filtering)
```

**API routes**

| Method | Path               | Description                          |
|--------|--------------------|--------------------------------------|
| GET    | `/quote`           | Random quote (optional filters)      |
| GET    | `/quote/categories`| List all categories                  |
| GET    | `/quote/authors`   | List all authors                     |
| GET    | `/quote/tags`      | List all tags                        |
| GET    | `/health`          | Liveness check                       |

Filter parameters for `GET /quote`: `?category=`, `?author=`, `?tag=`

See [docs/api.md](docs/api.md) for the full API contract with examples.

---

## Project structure

```
inspirational-quote-generator/
├── src/
│   ├── quotes/
│   │   ├── models.py        Quote dataclass
│   │   ├── data.py          Static quote dataset (30+ quotes, 8 categories)
│   │   └── service.py       QuoteService – retrieval & filtering
│   ├── handlers/
│   │   ├── api.py           Lambda handler – API Gateway proxy
│   │   └── scheduler.py     Lambda handler – EventBridge schedule
│   └── utils/
│       ├── logger.py        Structured JSON logger (CloudWatch-friendly)
│       ├── notifier.py      Webhook delivery (Slack/Discord, stdlib only)
│       └── response.py      HTTP response helpers
├── tests/
│   ├── test_models.py
│   ├── test_service.py
│   ├── test_api_handler.py
│   ├── test_notifier.py
│   └── test_scheduler_handler.py
├── infra/
│   ├── template.yaml        AWS SAM CloudFormation template
│   └── samconfig.toml       SAM deployment configuration
├── docs/
│   └── api.md               Full API contract documentation
├── .github/
│   └── workflows/
│       └── ci.yml           GitHub Actions CI (lint + test)
├── .env.example             Environment variable template
├── .gitignore
├── Makefile                 Developer shortcuts
├── requirements.txt         Runtime dependencies (none – stdlib only)
├── requirements-dev.txt     Development/test dependencies
├── setup.cfg                flake8 + pytest configuration
└── pyproject.toml           black configuration
```

---

## Quick start (local)

### Prerequisites

- Python 3.12+
- `make` (optional but recommended)

### Setup

```bash
git clone https://github.com/Abdul1452/inspirational-quote-generator.git
cd inspirational-quote-generator

# Install dev dependencies
make install-dev
# or: pip install -r requirements.txt -r requirements-dev.txt

# Copy environment template
cp .env.example .env
```

### Run locally

**Get a random quote:**
```bash
make run-local
```

**Simulate the daily scheduler:**
```bash
make run-scheduler
```

---

## Testing

```bash
# Run all tests with coverage
make test

# Quick run (no coverage)
make test-fast
```

---

## Linting & formatting

```bash
# Lint
make lint

# Auto-format
make format

# Check formatting (CI mode)
make format-check
```

---

## AWS Deployment

### Prerequisites

- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- AWS credentials configured (`aws configure` or environment variables)
- An S3 bucket (SAM will create one automatically with `resolve_s3 = true`)

### Deploy to dev

```bash
make deploy-dev
```

### Deploy to prod

```bash
make deploy-prod
```

After deployment, the API base URL is printed in the CloudFormation Outputs:

```
Outputs:
  ApiBaseUrl   = https://abc123.execute-api.us-east-1.amazonaws.com/dev
```

### Configuration parameters

| Parameter            | Default              | Description                                      |
|----------------------|----------------------|--------------------------------------------------|
| `Stage`              | `dev`                | Deployment stage (`dev` or `prod`)               |
| `LogLevel`           | `INFO`               | Lambda log level                                 |
| `ScheduleExpression` | `cron(0 8 * * ? *)` | EventBridge schedule (daily 08:00 UTC by default)|
| `NotifyWebhookUrl`   | `""` (disabled)      | Slack/Discord incoming webhook for the daily quote|

---

## Notifications

When `NOTIFY_WEBHOOK_URL` is set, the daily scheduler posts each quote to that
incoming webhook (Slack- and Discord-compatible) using only the Python standard
library. Delivery is best-effort: if the webhook is unreachable the error is
logged and the Lambda still succeeds. Leave the variable unset to disable
delivery — the quote is still written to CloudWatch.

Set it locally in `.env` (see `.env.example`), or at deploy time:

```bash
sam deploy --parameter-overrides NotifyWebhookUrl=https://hooks.slack.com/services/XXX/YYY/ZZZ
```

---

## Observability

Both Lambda functions emit structured JSON logs to CloudWatch:

```json
{
  "timestamp": "2026-01-01T08:00:01Z",
  "level":     "INFO",
  "logger":    "src.handlers.api",
  "message":   "Request completed",
  "status_code": 200,
  "elapsed_ms":  3.14
}
```

Log groups:
- `/aws/lambda/quote-generator-api-<stage>`
- `/aws/lambda/quote-generator-scheduler-<stage>`

Retention is set to 30 days.

---

## Contributing

1. Fork the repository and create a feature branch.
2. Make your changes with tests (`make test`).
3. Ensure lint passes (`make lint && make format-check`).
4. Open a pull request – CI runs automatically.

### Adding quotes

Edit `src/quotes/data.py`. Each quote uses the `Quote` dataclass:

```python
Quote(
    text="Your quote here.",
    author="Author Name",
    category="motivation",   # must be a string; new categories are auto-registered
    tags=["tag1", "tag2"],
    source="Optional book or URL",
)
```

Available categories: `courage`, `creativity`, `happiness`, `leadership`,
`mindfulness`, `motivation`, `perseverance`, `wisdom`.

---

## License

MIT
