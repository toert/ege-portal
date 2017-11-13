#!/bin/sh
cd /opt
source venv/bin/activate
cd ege-portal
gunicorn config.wsgi:application
