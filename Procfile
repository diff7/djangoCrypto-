web: gunicorn cryptoproject.wsgi --log-file -
worker: celery -A coinsapp.tasks worker --loglevel=info --concurrency=1


