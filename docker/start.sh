#!/bin/sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Wait for database to be ready
echo "Waiting for database..."
until nc -w 1 $DB_HOST 5432 >/dev/null 2>&1
do
    printf '.'
    sleep 1
done
echo

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start Gunicorn processes
echo "Starting Web Server"
uwsgi --http :8000 --module graphQLcore.wsgi --static-map /static=/app/static
