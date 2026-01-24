FROM python:3.13-slim

# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENTRYPOINT ["uv", "run"]

# curl для healthckeck'a:
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

RUN useradd --home-dir=/app --uid=1000 --user-group app
USER 1000

WORKDIR /app
ENV PYTHONPATH="/app/src:${PYTHONPATH}"

COPY --chown=app pyproject.toml alembic.ini uv.lock ./
RUN uv sync

COPY --chown=app migrations ./migrations

# Держать код в /app/src, а не в /app, чтобы в docker-compose.yml
# можно было мапить каталог с хоста в контейнер и использовать --reload
COPY --chown=app src ./src/

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port=8000", "--reload"]
