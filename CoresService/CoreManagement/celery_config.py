import os
from celery import Celery
from kombu import Exchange, Queue

""" Celery Configs"""


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CoreManagement.settings')
app = Celery('CoreManagement')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks',
          queue_arguments={'x-max-priority': 10}),
]
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
app.conf.broker_connection_retry_on_startup = True
app.conf.task_acks_late = True
app.conf.task_default_priority = 5
app.conf.worker_prefetch_multiplier = 1

# usually will set 2-4 times the number of CPU cores
app.conf.worker_concurrency = 1

app.autodiscover_tasks()
