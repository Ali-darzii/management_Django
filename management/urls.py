from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='projects')

urlpatterns = [] + router.urls
