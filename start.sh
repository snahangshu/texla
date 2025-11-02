#!/bin/bash
set -o errexit  # exit on error

# Move inside project directory
cd texla_service1

# Run Django management commands
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying migrations..."
python manage.py migrate --fake-initial

echo "Starting Gunicorn server..."
gunicorn texla_service.wsgi:application --bind 0.0.0.0:$PORT
