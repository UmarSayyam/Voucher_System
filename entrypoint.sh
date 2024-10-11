#!/bin/sh
#!/bin/sh

python manage.py migrate --no-input  # Run migrations
python manage.py collectstatic --no-input  # Collect static files

exec "$@"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files (optional for production)
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Start the Django development server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000




