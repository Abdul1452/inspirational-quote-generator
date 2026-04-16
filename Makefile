.PHONY: install install-dev test lint format format-check clean build deploy-dev deploy-prod

PYTHON   := python3
PIP      := $(PYTHON) -m pip
PYTEST   := $(PYTHON) -m pytest
BLACK    := $(PYTHON) -m black
FLAKE8   := $(PYTHON) -m flake8

# ── Setup ──────────────────────────────────────────────────────────────────────

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

install-dev: install
	$(PIP) install -r requirements-dev.txt

# ── Quality ────────────────────────────────────────────────────────────────────

lint:
	$(FLAKE8) src/ tests/

format:
	$(BLACK) src/ tests/

format-check:
	$(BLACK) --check src/ tests/

test:
	$(PYTEST) --tb=short --cov=src --cov-report=term-missing

test-fast:
	$(PYTEST) --tb=short -q

# ── Clean ──────────────────────────────────────────────────────────────────────

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	rm -rf .coverage coverage.xml htmlcov/ .pytest_cache/ .aws-sam/

# ── Local run ─────────────────────────────────────────────────────────────────

run-local:
	@echo '{"httpMethod":"GET","path":"/quote","queryStringParameters":{}}' \
	  | $(PYTHON) -c "import json,sys; from src.handlers.api import handler; print(json.dumps(handler(json.load(sys.stdin), None), indent=2))"

run-scheduler:
	@$(PYTHON) -c "import json; from src.handlers.scheduler import handler; print(json.dumps(handler({'source':'local','detail-type':'Manual'}, None), indent=2))"

# ── AWS SAM deploy ────────────────────────────────────────────────────────────

build:
	sam build --template-file infra/template.yaml --config-file infra/samconfig.toml

deploy-dev: build
	sam deploy --template-file .aws-sam/build/template.yaml \
	  --config-file infra/samconfig.toml \
	  --config-env default \
	  --parameter-overrides Stage=dev

deploy-prod: build
	sam deploy --template-file .aws-sam/build/template.yaml \
	  --config-file infra/samconfig.toml \
	  --config-env prod \
	  --parameter-overrides Stage=prod
