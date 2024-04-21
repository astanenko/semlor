#!/bin/sh

python manage.py collectstatic --clear --no-input;
python manage.py migrate;

gunicorn source.wsgi:application --workers 7 --bind 0.0.0.0:8000
