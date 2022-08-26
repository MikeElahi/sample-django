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

    def get_total_time_spent(self) -> int:
        """Get Total Time Spent on a Project

        Returns:
            int: total number of hours spent on project
        """
        duration = self.timelog_set.all().aggregate(models.Sum('duration'))['duration__sum']
        return duration // 3600 if duration else 0


class TimeLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    start_at = models.DateTimeField(null=True)
    finish_at = models.DateTimeField(null=True)
    duration = models.IntegerField(null=True)

    class Meta:
        ordering = ['id']

    def is_finished(self) -> bool:
        """Returns whether or not the timelog is finished

        Returns:
            bool
        """
        return self.duration is not None or \
            (self.start_at is not None and self.finish_at is not None)

    def status(self):
        """Determine the status of TimeLog"""
        if self.is_finished():
            return "FINISHED"
        if self.duration is None and self.start_at is not None:
            return "ONGOING"
        return "INVALID"

    def calculate_duration(self)-> int:
        """Calculates the duration between start and finish at

        Returns:
            int: number of seconds between the finish_at and start_at attributes
        """
        if self.finish_at is None or self.start_at is None:
            return self.duration
        return (self.finish_at - self.start_at).seconds

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.duration is None and \
            (self.is_finished() or self.duration != self.calculate_duration()):
            self.duration = self.calculate_duration()

        super().save(force_insert, force_update, using, update_fields)
