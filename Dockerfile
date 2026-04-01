# Stage 1: Build & Requirements
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY src /app/src

# Set Python path so `src` can be resolved
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "src.interfaces.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
