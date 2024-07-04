from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Project(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} | {self.created_at.year}"

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = 'Projects'
        db_table = 'projectTable'
        app_label = 'management'


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=225)
    description = models.TextField(null=True, default=None)

    status_choices = [('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')]
    status = models.CharField(choices=status_choices, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField()  # consider as deadline

    def __str__(self):
        return f"{self.project.name} | {self.title}"

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = 'Tasks'
        db_table = 'taskTable'



class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=225)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.project.name} | {self.task.title} | {self.author}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = 'Comments'
        db_table = 'commentTable'


# noif create and update Task to clients
@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    notification = {"type": "send_message", }
    if created:
        notification["message"] = f"{instance.title} Task created"
    else:
        notification["message"] = f"{instance.title}  Task updated"
    async_to_sync(channel_layer.group_send)("notifications", notification)


# noif deleted Task to clients
@receiver(post_delete, sender=Task)
def task_post_delete(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    notification = {"type": "send_message", "message": f"{instance.title}  Task deleted"}
    async_to_sync(channel_layer.group_send)("notifications", notification)


@receiver(post_save, sender=Comment)
def task_commented(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        notification = {"type": "send_message", "message": f"{instance.author} commented on {instance.task.title} task"}
        async_to_sync(channel_layer.group_send)("notifications", notification)
