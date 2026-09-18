# Amortize Platform POC

[![CI](https://github.com/mir-quadri/amortize-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/mir-quadri/amortize-platform/actions/workflows/ci.yml)

**What this proves**: End-to-end Python + Docker + Kubernetes + Terraform deployment at zero cloud cost, demonstrating production-grade SDLC practices with automated testing, linting, security scanning, and infrastructure-as-code.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Developer Workflow                      │
├─────────────────────────────────────────────────────────────┤
│ git push → GitHub Actions → Lint → Test → Build → Scan     │
│             ↓ (PR Checks)     ↓              ↓              │
│          Deploy to kind   GHCR Push      Smoke Test         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Local/CI Kubernetes Cluster (kind)             │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐  │
│  │           amortize namespace (Kustomize)            │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Deployment (2 replicas)                             │  │
│  │  ├─ amortize pod 1 ──┐                              │  │
│  │  └─ amortize pod 2 ──┤  ClusterIP Service :8000     │  │
│  │                      └──────────────────────────────│  │
│  │                                                      │  │
│  │  Health Checks:                                      │  │
│  │  • /healthz (liveness)                               │  │
│  │  • /readyz  (readiness)                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  Security Context (pod):                                    │
│  • runAsNonRoot: true (user 1000)                          │
│  • readOnlyRootFilesystem: true                            │
│  • ALL capabilities dropped                                 │
│                                                             │
│  Resource Limits:                                           │
│  • requests: 100m CPU, 128Mi memory                        │
│  • limits: 500m CPU, 512Mi memory                          │
└─────────────────────────────────────────────────────────────┘
```

## Service API

### POST /v1/amortization

Calculate amortization schedule for a loan.

**Request:**
```json
{
  "principal": 300000,
  "annual_rate_pct": 6,
  "term_months": 360
}
```

**Response:**
```json
{
  "monthly_payment": "1798.65",
  "total_interest": "347513.60",
  "schedule": [
    {
      "month": 1,
      "payment": "1798.65",
      "principal": "298.65",
      "interest": "1500.00",
      "balance": "299701.35"
    },
    ...
  ]
}
```

**Validation:**
- `principal > 0`
- `0 ≤ annual_rate_pct ≤ 50`
- `1 ≤ term_months ≤ 480`

### GET /healthz

Liveness probe. Returns `{"status": "ok"}` when service is running.

### GET /readyz

Readiness probe. Returns `{"status": "ready"}` when service can handle traffic.

## Tech Stack

- **Language**: Python 3.11
- **Web Framework**: FastAPI
- **Math**: Decimal (cents arithmetic, ROUND_HALF_UP)
- **Containerization**: Docker (multi-stage, slim base, <200MB)
- **Orchestration**: Kubernetes (plain manifests + Kustomize)
- **Infrastructure**: Terraform with kind provider
- **CI/CD**: GitHub Actions (lint → typecheck → test → docker build → scan → terraform → deploy → smoke)
- **Testing**: pytest with 90% coverage threshold
- **Code Quality**: ruff (lint+format), mypy (strict type checking)

## Design Decisions

### Why kind for Kubernetes?

- **Zero cost**: runs locally or in CI without cloud fees
- **Production-realistic**: full K8s with networking, persistent storage, RBAC
- **CI-friendly**: declarative, reproducible cluster provisioning via Terraform
- **Fast**: cluster up in <1 minute

### Why Decimal for money math?

- **Exactness**: Avoids floating-point rounding errors (e.g., 0.1 + 0.2 ≠ 0.3)
- **Standard**: Amortization formulas require precise cents arithmetic
- **Auditable**: Every payment computes to exactly 2 decimal places with ROUND_HALF_UP

### Why Terraform owns only the cluster?

- **Separation of concerns**: Terraform provisions infrastructure (kind cluster)
- **Declarative app deployment**: kubectl + Kustomize define app state (namespace, deployment, service, config)
- **CI simplicity**: `terraform apply` creates the cluster; `kubectl apply -k` deploys the app
- **Fast iteration**: Developers can re-deploy without `terraform apply`

## Quickstart

### Local Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
make test

# Lint and type check
make lint
make typecheck

# Build Docker image
make build

# Provision cluster and deploy
make up
make deploy

# Run smoke test
make smoke

# Clean up
make down
```

### CI/CD

Push to a PR or to `main` branch. GitHub Actions will:

1. **Lint** (ruff): Check code style
2. **Typecheck** (mypy): Verify type safety
3. **Test** (pytest): Run unit and integration tests (90% coverage required)
4. **Build** (docker): Multi-stage image, scan for vulnerabilities (Trivy: fail on HIGH/CRITICAL)
5. **Terraform**: fmt/validate, then apply to provision kind cluster
6. **Deploy** (kubectl + Kustomize): Apply manifests to cluster
7. **Smoke** (curl POST): Verify service returns correct payment for $300k/6%/360mo
8. **Publish** (on main only): Push image to `ghcr.io/mir-quadri/amortize-platform:${SHA}`

## File Structure

```
amortize-platform/
├── src/amortize/
│   ├── __init__.py
│   ├── calculator.py      # Core amortization logic
│   ├── app.py             # FastAPI application
│   └── main.py            # Entry point
├── tests/
│   ├── test_calculator.py # Unit tests
│   └── test_app.py        # API tests
├── k8s/
│   └── base/
│       ├── kustomization.yaml
│       ├── namespace.yaml
│       ├── deployment.yaml
│       ├── service.yaml
│       └── configmap.yaml
├── infra/
│   ├── versions.tf        # Terraform provider versions
│   ├── variables.tf       # Input variables
│   ├── main.tf            # kind cluster resource
│   └── outputs.tf         # Cluster info outputs
├── .github/workflows/
│   └── ci.yml             # GitHub Actions pipeline
├── Dockerfile
├── .dockerignore
├── Makefile
├── pyproject.toml
├── .gitignore
└── README.md
```

## Conventions

- **Commits**: Conventional commits (`feat:`, `fix:`, `test:`, `docs:`, etc.)
- **Python**: 
  - Black-compatible line length (100)
  - Type hints on all public functions (mypy strict mode)
  - Decimal for all currency/math
- **Kubernetes**: Plain manifests + Kustomize (no Helm, no operators)
- **Terraform**: 1.8+, pinned provider versions, no cloud backend

## Environment Variables

| Var | Default | Purpose |
|-----|---------|---------|
| `HOST` | `0.0.0.0` | HTTP bind address |
| `PORT` | `8000` | HTTP bind port |
| `WORKERS` | `1` | Uvicorn worker count |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Testing

- **Calculator**: Math verified against known values ($300k, 6%, 360mo → $1,798.65)
- **Edge cases**: Zero interest, 1-month term, very small principal, max bounds
- **API**: Validation, response structure, Decimal precision
- **Coverage**: 90% minimum enforced in CI

```bash
pytest tests/ --cov=src/amortize --cov-report=term-missing
```

## Security

- **Container**: Non-root user, read-only filesystem, no capabilities
- **Pod Security**: securityContext enforces least-privilege
- **Image Scanning**: Trivy scans for HIGH/CRITICAL vulnerabilities (CI gates on these)
- **Dependencies**: Pinned versions in pyproject.toml, no git sources

## Troubleshooting

### Docker build fails

Ensure `pyproject.toml` is valid:
```bash
python -m pip install -e .
```

### Kubernetes deployment doesn't roll out

Check pod events:
```bash
kubectl describe pod -n amortize
kubectl logs -n amortize -l app=amortize
```

### Smoke test fails

Port-forward and test manually:
```bash
kubectl port-forward -n amortize svc/amortize 8000:8000
curl -X POST http://localhost:8000/v1/amortization \
  -H "Content-Type: application/json" \
  -d '{"principal": 300000, "annual_rate_pct": 6, "term_months": 360}'
```

### Terraform plan fails

Ensure no stale state:
```bash
rm -f infra/*.tfstate* infra/.terraform.lock.hcl
cd infra && terraform init
```

## License

MIT

---

**Author**: Mir Quadri  
**POC Status**: ✓ End-to-end demo complete (Python→Docker→K8s→Terraform→CI)
