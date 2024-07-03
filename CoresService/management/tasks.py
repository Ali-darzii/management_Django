from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Task
from django.db.models import Q
from celery.signals import worker_ready
from django.core.cache import cache as redis


# run send_due_task_reminders after workers are up
@worker_ready.connect
def at_worker_ready(**kwargs):
    if not redis.get('send_due_task'):
        send_due_task_reminders.apply_async()
    redis.set('send_due_task', True)


# run send_due_task_reminders every 24 hour
@shared_task(queue='tasks')
def send_due_task_reminders():
    """ send email to remind them that they have 24 hour or less time """
    now = timezone.now()
    tomorrow = now + timedelta(days=1)
    due_tasks = Task.objects.filter(
        Q(due_date__range=[now, tomorrow]) & (Q(status='pending') | Q(status='in_progress')))

    for task in due_tasks:
        try:
            send_mail(
                'Task Due Reminder',
                f'The task "{task.title}" is due within the next 24 hours.',
                settings.DEFAULT_FROM_EMAIL,
                ['ali.darzi.1354@gmail.com'],
                fail_silently=False,
            )
        except:
            print("failed at sending email (redis)!!!")
