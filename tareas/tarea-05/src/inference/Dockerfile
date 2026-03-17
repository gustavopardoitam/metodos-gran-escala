FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY src ./src

#ENTRYPOINT ["python", "-m", "inference"]
ENTRYPOINT ["uv", "run", "python", "-m", "src.main", "--step"]
CMD ["predict"]
