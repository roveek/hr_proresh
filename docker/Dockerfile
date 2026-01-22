FROM python:3.13-slim

# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENTRYPOINT ["uv", "run"]

# curl для healthckeck'a:
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml alembic.ini uv.lock ./
RUN uv sync

COPY migrations ./migrations

COPY src ./

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
