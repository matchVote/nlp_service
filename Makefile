.PHONY: help

APP_VSN ?= `cat .version`

setup: ## Set up app locally
	docker-compose build

console: ## Start a console session
	docker-compose run --rm nlp python

test: ## Run the test suite
	docker-compose run --rm --service-ports -e NLP_ENV=test nlp python -m pytest

version: ## Show latest app version
	@echo $(APP_VSN)

build: ## Build the production Docker image
	docker build -t nlp_service:$(APP_VSN) .