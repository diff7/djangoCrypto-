web: gunicorn cryptoproject.wsgi --log-file -
worker: celery -A vcryptoproject worker -events -loglevel info 
beat: celery -A cryptoproject beat 
