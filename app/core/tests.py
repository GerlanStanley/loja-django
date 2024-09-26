from django.contrib.auth.models import User
from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIClient


class CommonTestCase(TestCase):
    def setUp(self):
        self.user = baker.make(
            User,
            username='usuario',
            password='12345678',
            email='teste@teste.com',
        )
        self.user.save()
        self.apiClient = APIClient()
        self.apiClient.force_authenticate(self.user)
