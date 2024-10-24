scene_dir = lorenz
scene_obj = LorenzAttractor

.PHONY: setup setdown install scene scene-hq clean
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
	manim -pql $(scene_dir)/lorenz.py $(scene_obj) --media_dir $(scene_dir)/media

scene-hq:
	manim -pqh $(scene_dir)/lorenz.py $(scene_obj) --media_dir $(scene_dir)/media

clean:
	rm -rf $(scene_dir)/media