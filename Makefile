.PHONY: test install-test install run
ifndef TAG
$(error The TAG variable is missing.)
endif


ACCOUNT := ardenerc
SERVICE := flaskapp
IMAGE := $(ACCOUNT)/$(SERVICE)

test:
	pytest -v
run:
	python app/app.py
install:
	cd app && pip install -r ./requirements.txt
install-test:
	make install
	pip install flake8 pytest
build:
	$(info Make: Building "$(TAG)" tagged images.)
		docker build -t $(IMAGE):$(TAG) .
		make -s tag
tag:
	$(info Make: Tagging image with "$(TAG)".)
	@docker tag $(IMAGE):latest $(IMAGE):$(TAG)
run:
	docker run -p $(PORT):80 $(IMAGE):$(TAG)