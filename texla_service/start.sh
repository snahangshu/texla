#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Run database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn server
gunicorn texla_service.wsgi:application --bind 0.0.0.0:$PORT
