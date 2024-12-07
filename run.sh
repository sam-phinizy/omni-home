#!/bin/sh
python manage.py migrate
gunicorn --bind :8000 --workers 2 omni_home.wsgi