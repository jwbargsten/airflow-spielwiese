.PHONY: lint fix test tags clean build docs
.DEFAULT_GOAL := help

AIRFLOW_VERSION=2.8.1

lint: ## lint the source code
	ruff check src/ tests/
	ruff format --check --exclude _version.py src/ tests/

fmt: ## format the source code with ruff
	ruff format src/ tests/
	ruff check --fix src/ tests/

install: ## install into current env
	pip install '.'

install-dev: ## install with dev dependencies
	pip install '.[dev]'

install-airflow:
	# PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
	# CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
	# pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

install-all: ## install with all dependencies (pyspark, airflow)
	pip install '.[all]'

test: ## run tests
	pytest tests/
	pytest -o pythonpath=dags/ dags_test/

tags: ## build a ctags file for jwb's crappy editor
	ctags --languages=python -f tags -R src tests

build: clean ## build the package (make sure you did `pip install '.[build]'` first)
	python -m build

clean: ## clean build artifacts and __pycache__ files up
	rm -rf dist/ build/ *.egg-info src/*.egg-info
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

help: ## this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9._-]+:.*?## / {printf "\033[1m\033[36m%-38s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

serve:
	AIRFLOW_CONN_SPARK_LOCAL='{"conn_type": "spark", "host": "local[2]", "extra": {"queue": "root.default"}}' \
	AIRFLOW_HOME=$(shell pwd)/airflow \
	airflow standalone
