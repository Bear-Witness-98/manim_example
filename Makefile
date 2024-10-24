.PHONY: setup setdown install
setup:		## Setup environment
	pip install virtualenv
	virtualenv .venv

setdown:
	rm -rf .venv

install:
	pip install -e .

install-dev:
	pip install -e .[dev]
