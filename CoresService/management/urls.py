from . import views
from rest_framework import routers
from django.urls import path

router = routers.DefaultRouter()

router.register(r'projects', views.ProjectViewSet, basename='projects')
router.register(r'tasks', views.TaskViewSet, basename='Tasks')
router.register(r'tasks/(?P<task_id>[^/.]+)/comments', views.CommentView, basename='Comments')

urlpatterns = [
                  path("ws_test/", views.ws_test_connection, name="room"),
              ] + router.urls
