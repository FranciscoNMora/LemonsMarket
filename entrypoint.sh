#!/bin/sh
#Check DB connection
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Flush DB
python manage.py flush --no-input
# Migrate
python manage.py migrate
# Run tests
python manage.py test --noinput
# Load default stocks
python manage.py loaddata stocks.yaml

python manage.py createsuperuser --no-input


exec "$@"