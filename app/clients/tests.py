from model_bakery import baker
from rest_framework import status

from app.clients.models import Client
from app.core.tests import CommonTestCase


class ClientTestCase(CommonTestCase):
    def setUp(self):
        super().setUp()
        self.client = baker.make(Client)
        self.client.save()
        self.base_url = '/api/v1/clients/'

    def test_get_all_clients_success(self):
        response = self.apiClient.get(self.base_url)

        self.assertTrue(response.status_code == status.HTTP_200_OK)
        data = response.json()
        self.assertTrue('results' in data)
        results = data['results']
        self.assertTrue(isinstance(results, list))
        self.assertTrue(len(results))
        self.assertTrue(results[0]['name'] == self.client.name)
        self.assertTrue(results[0]['email'] == self.client.email)

    def test_get_client_success(self):
        response = self.apiClient.get(self.base_url + f'{self.client.id}/')

        self.assertTrue(response.status_code == status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data['name'] == self.client.name)
        self.assertTrue(data['email'] == self.client.email)

    def test_get_client_404(self):
        response = self.apiClient.get(self.base_url + f'{self.client.id + 1}/')

        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND)

    def test_create_client_success(self):
        response = self.apiClient.post(
            self.base_url,
            data={
                'name': 'Lucas',
                'email': 'lucas@teste.com'
            },
        )

        self.assertTrue(response.status_code == status.HTTP_201_CREATED)

    def test_create_client_error_empty_data(self):
        response = self.apiClient.post(
            self.base_url,
            data={},
        )

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertTrue(data['name'] == ['This field is required.'])
        self.assertTrue(data['email'] == ['This field is required.'])

    def test_create_client_error_email_invalid(self):
        response = self.apiClient.post(
            self.base_url,
            data={
                'name': 'Lucas',
                'email': 'Teste',
            },
        )

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertTrue(data['email'] == ['Enter a valid email address.'])

    def test_create_client_error_with_email_exists(self):
        response = self.apiClient.post(
            self.base_url,
            data={
                'name': 'Lucas',
                'email': self.client.email,
            },
        )

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertTrue(data['email'] == ['Email already exists!'])

    def test_update_client_success(self):
        response = self.apiClient.put(
            self.base_url + f'{self.client.id}/',
            data={
                'name': 'João',
            },
        )

        self.assertTrue(response.status_code == status.HTTP_200_OK)
        data = response.json()
        print(data)
        self.assertTrue(data['name'] == 'João')

    def test_update_client_error_empty_data(self):
        response = self.apiClient.put(
            self.base_url + f'{self.client.id}/',
            data={},
        )

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertTrue(data['name'] == ['This field is required.'])
