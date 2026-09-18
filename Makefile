.PHONY: test lint typecheck build up deploy smoke down clean

test:
	python -m pytest tests/ -v --cov=src/amortize --cov-report=term-missing --cov-fail-under=90

lint:
	python -m ruff check src/ tests/

format:
	python -m ruff check --fix src/ tests/
	python -m ruff format src/ tests/

typecheck:
	python -m mypy src/

build: lint typecheck test
	docker build -t amortize:latest .

up:
	cd infra && terraform init && terraform apply -auto-approve

deploy: build
	kubectl kustomize k8s/base > /tmp/amortize-manifest.yaml
	kubectl apply -f /tmp/amortize-manifest.yaml
	kubectl rollout status deployment/amortize -n amortize --timeout=5m

smoke:
	@echo "Running smoke test..."
	@sleep 2
	@kubectl port-forward -n amortize svc/amortize 8000:8000 &
	@sleep 2
	@PAYMENT=$$(python -c "\
		import requests, json; \
		resp = requests.post('http://localhost:8000/v1/amortization', json={'principal': 300000, 'annual_rate_pct': 6, 'term_months': 360}); \
		print(json.loads(resp.text)['monthly_payment']); \
	"); \
	if [ "$$PAYMENT" = "1798.65" ]; then \
		echo "✓ Smoke test PASSED: Monthly payment = $$PAYMENT"; \
	else \
		echo "✗ Smoke test FAILED: Expected 1798.65, got $$PAYMENT"; \
		exit 1; \
	fi
	@pkill -f "kubectl port-forward" || true

down:
	cd infra && terraform destroy -auto-approve

clean: down
	docker rmi -f amortize:latest || true
	rm -f kubeconfig *.tfstate *.tfstate.backup

.DEFAULT_GOAL := test
