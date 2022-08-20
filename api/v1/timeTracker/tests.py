from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Project
from .serializers import ProjectSerializer

class ProjectsTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='TestingUser')
        self.project = Project.objects.create(slug='TestingProject')
        self.project.users.add(self.user)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_api_can_index_projects(self):
        response = self.client.get(reverse('project-list'))
        assert response.status_code == 200
        self.assertEqual(ProjectSerializer(self.project).data, response.json()['results'][0])

    def test_api_can_get_project(self):
        response = self.client.get(reverse('project-detail', args=[self.project.pk]))
        assert response.status_code == 200
        self.assertEqual(ProjectSerializer(self.project).data, response.json())

    def test_api_can_create_project(self):
        response = self.client.post(reverse('project-list'), {
            'title': 'Testing!',
            'slug': 'a-sample-slug',
            'users': [self.user.pk, ],
        })
        assert response.status_code == 201
        self.assertEqual(Project.objects.filter(users=self.user).count(), 2)

    def test_api_can_delete_project(self):
        response = self.client.delete(reverse('project-detail', args=[self.project.pk]))
        assert response.status_code == 204
        self.assertEqual(Project.objects.filter(users=self.user).count(), 0)

    def test_api_can_update_project(self):
        data = ProjectSerializer(self.project).data
        data['title'] = 'New Title'

        response = self.client.put(reverse('project-detail', args=[self.project.pk]), data)

        assert response.status_code == 200
        self.assertTrue(Project.objects.filter(users=self.user, title__exact=data['title']).exists())