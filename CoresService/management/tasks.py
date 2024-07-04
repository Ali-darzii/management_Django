from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Task, Project, Comment
from django.db.models import Q
from celery.signals import worker_ready
from django.core.cache import cache as redis
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

recipient_email = 'ali.darzi.1354@gmail.com'


# run functions after celery workers are up
@worker_ready.connect
def at_worker_ready(**kwargs):
    if not redis.get('run_for_once'):
        send_due_task_reminders.apply_async()
        daily_project_summery.apply_async()
    redis.set('run_for_once', True)


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
                [recipient_email],
                fail_silently=False,
            )
        except:
            redis.set(f"{recipient_email}_not_sent", 1)


@shared_task(queue='tasks')
def daily_project_summery():
    """ Summery of Projects every 24 hour"""
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    summery_body = ''
    projects = Project.objects.all()
    for project in projects:
        summery_body = f'Project: {project.name}\n'
        tasks = Task.objects.filter(project=projects, due_date__lte=tomorrow)
        if tasks.exists():
            summery_body += 'Tasks:\n'
            for task in tasks:
                summery_body += f'- {task.title}: {task.status}\n'
                comments = Comment.objects.filter(task=task)
                if comments.exists():
                    summery_body += '  Comments:\n'
                    for comment in comments:
                        summery_body += f'    - {comment.author}: {comment.content}\n'
    # or we can send email
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("notifications",
                                            {"type": "send_message", "message": "Project Summary arrived"})
    print(summery_body)
