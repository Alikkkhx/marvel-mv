#!/usr/bin/env bash
# Used by Render / similar hosts: install deps, static files, migrations
set -e
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
