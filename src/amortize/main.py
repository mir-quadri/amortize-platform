"""Application entry point."""

import os

import uvicorn

if __name__ == "__main__":  # pragma: no cover
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    workers = int(os.getenv("WORKERS", "1"))

    uvicorn.run(
        "amortize.app:app",
        host=host,
        port=port,
        workers=workers,
        access_log=False,
    )
