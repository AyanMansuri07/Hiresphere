#!/usr/bin/env bash

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Start Gunicorn server
gunicorn Hiresphere.wsgi:application
