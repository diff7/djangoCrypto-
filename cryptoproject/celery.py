from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptoproject.settings')

app = Celery('cryptoproject')

app.conf.update(
    result_expires=60,
    task_acks_late=True,
    broker_url='redis://localhost:6379',
    #result_backend='redis://localhost',

                )

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
celery = Celery('task', broker='redis://127.0.0.1:6379')

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
