ARG PYTHON_VERSION=3

FROM python:$PYTHON_VERSION as builder

WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install pip install --user --no-cache-dir -r requirements.txt

# ---

FROM python:$PYTHON_VERSION-slim

RUN useradd -ms /bin/bash app

USER app

COPY --from=builder --chown=app /root/.local /home/app/.local

WORKDIR /app

COPY src /app/src

ENV GPIOZERO_PIN_FACTORY=pigpio

ENTRYPOINT [ "python3", "src/main.py" ]
