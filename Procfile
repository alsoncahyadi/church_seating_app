release: python manage.py migrate
web: daphne seating_site.asgi:application --port $PORT --bind 0.0.0.0
worker: python manage.py runworker channels
