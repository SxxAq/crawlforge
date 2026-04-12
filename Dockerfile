FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

COPY pyproject.toml uv.lock ./
COPY . .
RUN uv sync --frozen --no-dev

CMD ["uv", "run", "python", "-m", "crawlforge.main"]
