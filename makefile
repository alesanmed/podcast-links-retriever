.PHONY: start
start:
	poetry run python main.py

.PHONY: shell
shell:
	poetry shell

.PONY: build
build:
	poetry export -o requirements.txt --without-hashes
	docker build .