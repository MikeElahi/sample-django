from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    title = models.TextField(null=False, help_text="Required, Title of your project")
    slug = models.SlugField()
    users = models.ManyToManyField(User)

class TimeLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_at = models.DateTimeField(null=True)
    finish_at = models.DateTimeField(null=True)
    duration = models.IntegerField(null=True)
