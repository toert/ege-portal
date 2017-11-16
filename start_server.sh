#!/bin/sh
cd /opt
source venv/bin/activate
cd ege-portal
export DJANGO_SETTINGS_MODULE=config.settings.production
gunicorn config.wsgi:application
