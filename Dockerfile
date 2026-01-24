FROM python:3.14-slim

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.9.2 /uv /uvx /bin/

ENV PYTHONBUFFER=1
# Compiles bytecode for improved startup times for the container at the cost of build time and size
ENV UV_COMPILE_BYTECODE=1

WORKDIR /app

# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

COPY ./pyproject.toml ./uv.lock /app/

# Install dependencies
# ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY ./alembic.ini /app/
COPY ./omninomicon /app/omninomicon

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

CMD ["uv", "run", "/app/omninomicon/main.py"]
