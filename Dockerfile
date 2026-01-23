FROM python:3.14-slim

ENV PYTHONBUFFER=1

WORKDIR /app

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.9.2 /uv /uvx /bin/

# Place executables in the environment at the front of the path
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

COPY ./pyproject.toml ./uv.lock /app/
COPY ./omninomicon /app/omninomicon

RUN uv sync --frozen --no-cache

CMD ["uv", "run", "/app/omninomicon/main.py"]
