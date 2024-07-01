from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='projects')
router.register(r'tasks', views.TaskViewSet, basename='Tasks')

urlpatterns = [] + router.urls
