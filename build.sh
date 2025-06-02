npm install
python manage.py tailwind install
python manage.py tailwind build

# Apply database migrations
python manage.py migrate

# Collect static files (for admin panel and Tailwind)
python manage.py collectstatic --noinput