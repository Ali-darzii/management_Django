from rest_framework import viewsets
from rest_framework.serializers import ValidationError

from .models import Project, Task, Comment
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer
from rest_framework.viewsets import mixins, GenericViewSet


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


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
