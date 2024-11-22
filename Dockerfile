ARG PYTHON_VERSION=3

FROM python:$PYTHON_VERSION AS builder

ARG POETRY_VERSION=1.8.4
RUN pip install poetry==${POETRY_VERSION}

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR \
    poetry install --no-root

# ---

# FROM builder AS runner

# ENV VIRTUAL_ENV=/app/.venv \
#     PATH="/app/.venv/bin:$PATH"

# ENV GPIOZERO_PIN_FACTORY=pigpio

# ---

FROM python:$PYTHON_VERSION-slim

RUN useradd -ms /bin/bash app

USER app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app

COPY src /app/src

ENV GPIOZERO_PIN_FACTORY=pigpio

ENTRYPOINT [ "python3", "-u", "src/main.py" ]
