#!/bin/bash
cd texla_service1
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn texla_service.wsgi:application --bind 0.0.0.0:$PORT
