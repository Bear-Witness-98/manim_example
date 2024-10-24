.PHONY: setup setdown install scene
setup:		## Setup environment
	pip install virtualenv
	virtualenv .venv

setdown:
	rm -rf .venv

install:
	pip install -e .

install-dev:
	pip install -e .[dev]

scene:
	manim -pql lorenz/lorenz.py LorenzAttractor
