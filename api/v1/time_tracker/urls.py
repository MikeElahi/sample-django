from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from config.settings import DEBUG
from .views import ProjectViewSet, UserViewSet, TimeLogViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'timelogs', TimeLogViewSet, basename='timelog')

if DEBUG:
    router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
