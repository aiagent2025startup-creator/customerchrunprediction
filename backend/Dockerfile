FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (libgomp1 is required for LightGBM)
RUN apt-get update && apt-get install -y \
  curl \
  libgomp1 \
  && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY training/ ./training/
COPY frontend/ ./frontend/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
