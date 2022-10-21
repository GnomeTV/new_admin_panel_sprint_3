#!/usr/bin/env bash

set -e

chown www-data:www-data /var/log
python manage.py collectstatic --noinput
sleep 5
python manage.py migrate
apt update
apt install gettext --assume-yes
python manage.py compilemessages -l en -l ru
uwsgi --strict --ini /opt/app/uwsgi/uwsgi.ini
