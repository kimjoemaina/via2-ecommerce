#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

uwsgi --ini uwsgi.ini