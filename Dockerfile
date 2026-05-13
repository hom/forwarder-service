FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir .

COPY app/ ./app/
COPY main.py ./

EXPOSE 8000

CMD ["python", "main.py"]
