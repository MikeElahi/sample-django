from django.urls import include, path
from rest_framework import routers
from .views import ProjectViewSet, UserViewSet, TimeLogViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'users', UserViewSet, basename='user')
router.register(r'timelogs', TimeLogViewSet, basename='timelog')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]