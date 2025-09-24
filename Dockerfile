FROM ghcr.io/astral-sh/uv:0.8.22-python3.12-bookworm-slim

ADD . /app

# Assuming the lockfile is up to date
WORKDIR /app
RUN uv sync --locked

CMD ["uv", "run", "main.py"]