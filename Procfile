web: gunicorn cryptoproject.wsgi --log-file -
worker: celery -A cryptoproject worker -events -log level info 
beat: celery -A cryptoproject beat 
