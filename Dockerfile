# Set the python version
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Create a virtual environment
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install os dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    libcairo2 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /code

# Copy the requirements file and install them
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN pip install gunicorn

# Copy the project code
COPY ./src /code

# Set arguments and environment variables
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}  

ARG DJANGO_DEBUG=0  
ENV DJANGO_DEBUG=${DJANGO_DEBUG}

# Set the Django default project name
ARG PROJ_NAME="cfehome"

# Run static files and vendor tasks
RUN python manage.py vendor_pull
RUN python manage.py collectstatic --noinput

# --- CORRECTED SCRIPT CREATION ---
# 'EOF' er pashe single quote dile variable gulo build-time e change hobe na
RUN cat <<'EOF' > ./paracord_runner.sh
#!/bin/bash
RUN_PORT=${PORT:-8080}
echo "Starting Gunicorn on port $RUN_PORT"
python manage.py migrate --no-input
gunicorn ${PROJ_NAME:-cfehome}.wsgi:application --bind 0.0.0.0:$RUN_PORT
EOF

# make the bash script executable
RUN chmod +x paracord_runner.sh

# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run the Django project
CMD ["./paracord_runner.sh"]