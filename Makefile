.PHONY: commit lint install check

XARGS := $(if $(shell echo | xargs -r 2>/dev/null && echo 1), xargs -r, xargs)
GIT_DIFF := git diff --name-only --cached --diff-filter=dt

commit:
	${GIT_DIFF} -- '*.py' | ${XARGS} isort --check-only --diff
	${GIT_DIFF} -- '*.py' | ${XARGS} flake8

lint:
	isort --check-only --diff ./border_radius ./test_border_radius.py
	flake8 ./border_radius ./test_border_radius.py

install:
	pip install pip==19.3.1 setuptools==42.0.2 wheel==0.33.6
	pip install -e .[dev]

check:
	pytest --cov-report=term:skip-covered --cov-report=html --cov-fail-under=100 --cov=border_radius
