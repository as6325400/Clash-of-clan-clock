#!/usr/bin/env bash
set -e 

echo "Waiting for DB (mariadb:3306) to be ready..."
./wait-for-it.sh mariadb:3306 -t 30 -- echo "DB is up!"

alembic upgrade head
gunicorn -w 4 -b 0.0.0.0:5000 app:app

echo "Starting my app..."
exec "$@"
