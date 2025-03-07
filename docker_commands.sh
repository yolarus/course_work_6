#!/bin/bash

python manage.py migrate && \
python manage.py load_users && \
python manage.py load_habits  && \
python manage.py collectstatic --noinput && \
gunicorn config.wsgi:application --bind 0.0.0.0:8000