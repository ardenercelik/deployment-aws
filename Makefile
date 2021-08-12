.PHONY: test install-test install run

test:
	pytest -v
run:
	python app/app.py
install:
	cd app && pip install -r ./requirements.txt
install-test:
	make install
	pip install flake8 pytest

