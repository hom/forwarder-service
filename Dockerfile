FROM python:3.13-slim

WORKDIR /app

# Install dependencies via pip
COPY pyproject.toml ./
RUN pip install --no-cache-dir fastapi uvicorn python-dotenv

# Copy application code
COPY app/ ./app/
COPY main.py ./

EXPOSE 8000

CMD ["python", "main.py"]
