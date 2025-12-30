#!/usr/bin/env bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn Hireshpere.wsgi:application
