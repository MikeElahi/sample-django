from unittest import TestCase
from datetime import timedelta
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from .models import Project, TimeLog
from .serializers import ProjectSerializer


class AbstractProjectTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = get_user_model().objects.create(username=get_random_string(16))
        cls.project = Project.objects.create(slug='TestingProject')
        cls.project.users.add(cls.user)


class ProjectsAPITest(AbstractProjectTestCase, APITestCase):
    """"Integration Tests for Projects API"""

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_api_can_index_projects(self):
        """API GET /projects/"""
        response = self.client.get(reverse('project-list'))
        assert response.status_code == 200
        self.assertEqual(ProjectSerializer(self.project).data,
                         response.json()['results'][0])

    def test_api_can_get_project(self):
        """API GET /projects/:id"""
        response = self.client.get(
            reverse('project-detail', args=[self.project.pk]))
        assert response.status_code == 200
        self.assertEqual(ProjectSerializer(self.project).data, response.json())

    def test_api_can_create_project(self):
        """API POST /projects/"""
        response = self.client.post(reverse('project-list'), {
            'title': 'Testing!',
            'slug': 'a-sample-slug',
            'users': [self.user.pk, ],
        })
        assert response.status_code == 201
        self.assertEqual(Project.objects.filter(users=self.user).count(), 2)

    def test_api_can_delete_project(self):
        """API DELETE /projects/:id"""
        response = self.client.delete(
            reverse('project-detail', args=[self.project.pk]))
        assert response.status_code == 204
        self.assertEqual(Project.objects.filter(users=self.user).count(), 0)

    def test_api_can_update_project(self):
        """API PUT /projects/:id"""
        data = ProjectSerializer(self.project).data
        data['title'] = 'New Title'

        response = self.client.put(
            reverse('project-detail', args=[self.project.pk]), data)

        assert response.status_code == 200
        self.assertTrue(Project.objects.filter(
            users=self.user, title__exact=data['title']).exists())


class TimeLogStatusMethodsTest(AbstractProjectTestCase):
    STATUS_CASES = [
        ["FINISHED", {'duration': 10}],
        ["FINISHED", {'start_at': timezone.now().replace(minute=0),
         'finish_at': timezone.now().replace(minute=50)}],
        ['ONGOING', {'start_at': timezone.now()}],
        ['INVALID', {}],
        ['INVALID', {'duration': None, 'start_at': None}],
    ]

    def test_can_calculate_status(self):
        """Unit Test on Computed Status Field"""
        for case in self.STATUS_CASES:
            timelog = TimeLog.objects.create(
                project=self.project, user=self.user, **case[1])
            assert timelog.status() == case[0]

    def test_can_determine_is_finished(self):
        """Unit Test on is_finished"""
        for case in self.STATUS_CASES:
            timelog = TimeLog.objects.create(
                project=self.project, user=self.user, **case[1])
            assert timelog.is_finished() == (case[0] == 'FINISHED')


class TimeLogDurationCalculation(AbstractProjectTestCase):
    def test_can_calculate_duration(self):
        """Unit Test for calculate_duration method on Timelog model"""
        timelog = TimeLog.objects.create(project=self.project, user=self.user,
                                         start_at=timezone.now(),
                                         finish_at=timezone.now() + timedelta(hours=5))
        assert timelog.duration == 5 * 3600

    def test_can_calculate_duration_before_save(self):
        """Unit Test for changes in save method in Timelog Model"""
        timelog = TimeLog.objects.create(project=self.project, user=self.user,
                                         start_at=timezone.now())

        timelog.finish_at = timezone.now() + timedelta(hours=5)
        timelog.save()
        assert timelog.duration == 5 * 3600


class ProjectTotalTimeTest(AbstractProjectTestCase):
    def test_can_get_total_time_spent(self):
        "Unit test for get_total_time_spent"
        target_hours = 5
        for _ in range(target_hours):
            TimeLog.objects.create(project=self.project, user=self.user,
                                   duration=3600)

        assert self.project.get_total_time_spent() == target_hours
