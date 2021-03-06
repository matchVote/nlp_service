.PHONY: help

APP_VSN ?= `cat .version`

help:
	@echo nlp_service:$(APP_VSN)
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

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

heroku-push: ## Use Heroku to build production image and push to registry
	heroku container:push web --verbose --app mv-nlp

heroku-release: ## Deploy container from previously pushed image
	heroku container:release web --app mv-nlp
