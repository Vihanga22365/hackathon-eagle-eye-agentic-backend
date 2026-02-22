# ── Stage 1: Build ────────────────────────────────────────────────────
FROM python:3.13-slim AS builder

WORKDIR /app

# System deps required by faiss-cpu and unstructured[pdf]
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    poppler-utils \
    tesseract-ocr \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manifest and install into a prefix directory
COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install .


# ── Stage 2: Runtime ──────────────────────────────────────────────────
FROM python:3.13-slim

WORKDIR /app

# Runtime system libraries only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    poppler-utils \
    tesseract-ocr \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY . .

# Cloud Run injects PORT; default to 8350 for local runs
ENV PORT=8350

EXPOSE 8350

# main.py already reads os.environ.get("PORT", 8350)
CMD ["python", "main.py"]
