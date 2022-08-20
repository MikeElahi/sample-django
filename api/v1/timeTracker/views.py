from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Project, TimeLog
from .serializers import ProjectSerializer, UserSerializer, TimeLogSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

class TimeLogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TimeLogSerializer

    def get_queryset(self):
        return TimeLog.objects.filter(project__users=self.request.user).filter(user=self.request.user)