from django.db import models
from django.contrib.auth import get_user_model


class Project(models.Model):
    title = models.TextField(
        null=False, help_text="Required, Title of your project")
    slug = models.SlugField()
    users = models.ManyToManyField(get_user_model())

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return str(self.title)


class TimeLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    start_at = models.DateTimeField(null=True)
    finish_at = models.DateTimeField(null=True)
    duration = models.IntegerField(null=True)

    class Meta:
        ordering = ['id']

    def status(self):
        if self.duration is not None or (self.start_at is not None and self.finish_at is not None):
            return "FINISHED"
        if self.duration is None and self.start_at is not None:
            return "ONGOING"
        return "INVALID"
