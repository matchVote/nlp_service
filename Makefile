.PHONY: help

test: ## Run the test suite
	docker-compose run --rm nlp python -m pytest