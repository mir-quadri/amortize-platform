FROM python:3.11-slim as builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --target /build/lib .


FROM python:3.11-slim

WORKDIR /app

RUN groupadd -r -g 1000 app && useradd -r -u 1000 -g 1000 app

COPY --from=builder /build/lib /usr/local/lib/python3.11/site-packages

COPY src/amortize ./amortize

RUN chown -R app:app /app && \
    chmod -R 555 /app && \
    chmod -R 444 /app/amortize

USER app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOST=0.0.0.0 \
    PORT=8000 \
    WORKERS=1 \
    LOG_LEVEL=INFO

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz').read()" || exit 1

ENTRYPOINT ["python", "-m", "amortize.main"]
