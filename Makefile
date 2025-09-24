build-deps:
	@python3 -c "import pygame" 2>/dev/null || (echo 'Installing pygame...' && pip install pygame)
	@python3 -c "import cairosvg" 2>/dev/null || (echo 'Installing cairosvg...' && pip install pygame)

run: build-deps dvd-logo.svg
	python3 main.py
