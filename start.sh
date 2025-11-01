#!/bin/bash
python texla_service/manage.py collectstatic --noinput
python texla_service/manage.py migrate
gunicorn texla_service1.texla_service.wsgi:application --bind 0.0.0.0:$PORT
