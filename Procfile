web: gunicorn cryptoproject.wsgi --log-file -
worker: python manage.py celery worker --loglevel=info
celery_beat: python manage.py celery beat --loglevel=info


