from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project
from .models import TimeLog

class ProjectPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    requires_context = True
    def get_queryset(self):
        return Project.objects.filter(users=self.context.get('request').user)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'users']


class TimeLogSerializer(serializers.ModelSerializer):
    project = ProjectPrimaryKeyRelatedField()
    start_at = serializers.DateTimeField(allow_null=True)
    finish_at = serializers.DateTimeField(allow_null=True)
    status = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField('timelog-detail')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TimeLog
        fields = ['id', 'project', 'start_at', 'finish_at', 'duration', 'status', 'url', 'user']

    def validate(self, attrs):
        if attrs['duration'] is None and attrs['start_at'] is None:
            raise serializers.ValidationError("Duration and Start At cannot be null at the same time")
        if  attrs['start_at'] is not None and attrs['finish_at'] is not None and attrs['start_at'] > attrs['finish_at']:
            raise serializers.ValidationError("Finish At cannot be larger than start_at")
        return attrs

