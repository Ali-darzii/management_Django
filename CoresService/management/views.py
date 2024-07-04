from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.serializers import ValidationError
from .models import Project, Task, Comment
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer
from rest_framework.viewsets import mixins, GenericViewSet
from django.core.cache import cache as redis
from django.conf import settings
from rest_framework.response import Response


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def list(self, request, *args, **kwargs):
        # Check if projects are already cached
        projects = redis.get('cached_projects')
        if not projects:
            print("not using catch")
            projects = list(self.get_queryset().values())
            redis.set('cached_projects', projects, timeout=settings.CACHE_TIMEOUT)
        return Response(projects)

    # cache project after created
    def perform_create(self, serializer):
        serializer.save()
        redis.delete('cached_projects')

    # cache project after updated
    def perform_update(self, serializer):
        serializer.save()
        redis.delete('cached_projects')

    # flush project after deleted
    def perform_destroy(self, instance):
        instance.delete()
        redis.delete('cached_projects')


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    # cache the list of projects
    def list(self, request, *args, **kwargs):
        tasks = redis.get('cached_tasks')
        if not tasks:
            tasks = list(self.get_queryset().values())
            redis.set('cached_tasks', tasks, timeout=settings.CACHE_TIMEOUT)
        return Response(tasks)

    # same as project cache performing
    def perform_create(self, serializer):
        serializer.save()
        redis.delete('cached_tasks')

    def perform_update(self, serializer):
        serializer.save()
        redis.delete('cached_tasks')

    def perform_destroy(self, instance):
        instance.delete()
        redis.delete('cached_tasks')


class CommentView(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        task_id = self.kwargs["task_id"]
        return Comment.objects.filter(task_id=task_id)

    def create(self, request, *args, **kwargs):
        try:
            task_id = int(self.kwargs["task_id"])
        except ValueError:
            raise ValidationError(detail="task id format is not right")

        request.data["task"] = task_id
        return super().create(request, *args, **kwargs)


def ws_test_connection(request):
    return render(request, "management/ws_test.html", )

