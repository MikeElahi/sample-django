from django.utils import timezone
from unittest import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from .models import Project, TimeLog
from .serializers import ProjectSerializer


class ProjectsAPITest(APITestCase):
    """"Integration Tests for Projects API"""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(username='TestingUser')
        self.project = Project.objects.create(slug='TestingProject')
        self.project.users.add(self.user)

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


class TimeLogStatusTest(TestCase):
    CASES = [
        ["FINISHED", {'duration': 10}],
        ["FINISHED", {'start_at': timezone.now().replace(minute=0),
         'finish_at': timezone.now().replace(minute=50)}],
        ['ONGOING', {'start_at': timezone.now()}],
        ['INVALID', {}],
        ['INVALID', {'duration': None, 'start_at': None}],
    ]

    def setUp(self) -> None:
        super().setUp()
        self.user = get_user_model().objects.create(username='TestingUser')
        self.project = Project.objects.create(slug='TestingProject')
        self.project.users.add(self.user)

    def test_can_calculate_status(self):
        for case in self.CASES:
            timelog = TimeLog.objects.create(project=self.project, user=self.user, **case[1])
            assert timelog.status() == case[0]
