# Set the python version as a build-time argument
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Create a virtual environment
RUN python -m venv /opt/venv

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHON_BUFFERED 1

# Install os dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    libcairo2 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create and set the working directory
RUN mkdir -p /code
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

# --- Fix for the $PORT error starts here ---
# create a bash script to run the Django project
RUN echo '#!/bin/bash' > ./paracord_runner.sh && \
    echo 'RUN_PORT=${PORT:-8080}' >> ./paracord_runner.sh && \
    echo 'python manage.py migrate --no-input' >> ./paracord_runner.sh && \
    echo "gunicorn ${PROJ_NAME}.wsgi:application --bind 0.0.0.0:\$RUN_PORT" >> ./paracord_runner.sh

# make the bash script executable
RUN chmod +x paracord_runner.sh
# --- Fix ends here ---

# Clean up apt cache
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run the Django project via the runner script
CMD ["./paracord_runner.sh"]