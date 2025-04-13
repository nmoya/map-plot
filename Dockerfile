FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install uv
RUN pip install uv

# Copy your dependency definitions
COPY pyproject.toml ./

# Install dependencies globally
RUN uv pip install . --system

# Copy the actual app code
COPY . .

EXPOSE 8080

# Run the app
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8080"]
