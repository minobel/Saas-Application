# -----------------------------
# Base image
# -----------------------------
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# -----------------------------
# Python & env setup
# -----------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# -----------------------------
# System dependencies
# -----------------------------
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    libcairo2 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# App directory
# -----------------------------
WORKDIR /code

# -----------------------------
# Python dependencies
# -----------------------------
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN pip install gunicorn rav --upgrade

# -----------------------------
# Copy project
# -----------------------------
COPY ./src /code
COPY ./rav.yaml /tmp/rav.yaml

# -----------------------------
# Static files (build-time)
# -----------------------------
RUN rav download staticfiles_prod -f /tmp/rav.yaml
RUN python manage.py collectstatic --noinput

# -----------------------------
# Runtime env vars (platform will override)
# -----------------------------
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

ARG DJANGO_DEBUG=0
ENV DJANGO_DEBUG=${DJANGO_DEBUG}

# -----------------------------
# Startup script
# -----------------------------
ARG PROJ_NAME="cfehome"

RUN printf "#!/bin/sh\n" > /code/paracord_runner.sh && \
    printf "set -e\n" >> /code/paracord_runner.sh && \
    printf "RUN_PORT=\${PORT:-8000}\n\n" >> /code/paracord_runner.sh && \
    printf "python manage.py migrate --no-input\n" >> /code/paracord_runner.sh && \
    printf "exec gunicorn ${PROJ_NAME}.wsgi:application --bind 0.0.0.0:\$RUN_PORT --workers 2 --threads 4 --timeout 120\n" >> /code/paracord_runner.sh

RUN chmod +x /code/paracord_runner.sh

# -----------------------------
# Run app
# -----------------------------
CMD ["sh", "-c", "/code/paracord_runner.sh"]
