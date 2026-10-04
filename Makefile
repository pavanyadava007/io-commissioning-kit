PY ?= .venv/bin/python
UV ?= uv

.PHONY: setup lint test docs loopcheck cetest campaign results site all

setup:
	$(UV) venv --python 3.11 .venv
	$(UV) pip install --python $(PY) -e ".[dev]"

lint:
	$(PY) -m ruff check .
	$(PY) -m iokit.cli lint

test:
	$(PY) -m pytest -q

docs:
	$(PY) -m iokit.cli docs

loopcheck:
	$(PY) -m iokit.cli loopcheck --faults config/demo_faults.yaml --out results/sample_run

cetest:
	$(PY) -m iokit.cli cetest --out results/cetest

campaign:
	$(PY) scripts/run_campaign.py --n 200 --seed 1

results:
	$(PY) scripts/make_results.py
	$(PY) scripts/build_site.py

all: lint test docs loopcheck cetest campaign results
