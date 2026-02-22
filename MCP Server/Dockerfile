# ── Stage 1: Build ────────────────────────────────────────────────────
FROM python:3.13-slim AS builder

WORKDIR /app

# System deps required by faiss-cpu
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manifest and install into a prefix directory
COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install .


# ── Stage 2: Runtime ──────────────────────────────────────────────────
FROM python:3.13-slim

WORKDIR /app

# Runtime system library for faiss-cpu (OpenMP)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source (includes rag/faiss_db index files)
COPY . .

# MCP server listens on 8351; Cloud Run is configured with --port 8351
EXPOSE 8351

CMD ["python", "main.py"]
