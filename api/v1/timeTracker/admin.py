"""Admin Registrations for TimeTracker App"""
from django.contrib import admin
from .models import Project, TimeLog


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Project Admin Registrar Class"""


@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
    """TimeLog Model Admin Registrar Class"""
