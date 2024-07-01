from rest_framework import viewsets
from management.models import Project
from management.serializers import ProjectSerializer


# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
