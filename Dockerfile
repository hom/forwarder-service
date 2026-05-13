FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml main.py ./
COPY app/ ./app/
RUN pip install --no-cache-dir .

CMD ["python", "main.py"]
