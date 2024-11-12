scene_dir = lorenz
scene_obj = LorenzAttractor
test_dir = test
test_obj = TestScene

.PHONY: setup setdown install scene scene-hq clean test test-hq
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

test:
	manim -pql $(test_dir)/test.py $(test_obj) --media_dir $(test_dir)/media

test-hq:
	manim -pqh $(test_dir)/test.py $(test_obj) --media_dir $(test_dir)/media

clean:
	rm -rf $(scene_dir)/media
	rm -rf $(test_dir)/media