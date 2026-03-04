FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY src ./src

CMD ["python", "-m", "processing"]