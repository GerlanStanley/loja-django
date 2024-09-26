from model_bakery import baker
from rest_framework import status

from app.products.models import Product
from app.core.tests import CommonTestCase


class ProductTestCase(CommonTestCase):
    def setUp(self):
        super().setUp()
        self.product = baker.make(Product)
        self.product.save()
        self.base_url = '/api/v1/products/'

    def test_get_all_products_success(self):
        response = self.apiClient.get(self.base_url)

        self.assertTrue(response.status_code == status.HTTP_200_OK)
        data = response.json()
        self.assertTrue('results' in data)
        results = data['results']
        self.assertTrue(isinstance(results, list))
        self.assertTrue(len(results))
        self.assertTrue(results[0]['name'] == self.product.name)
        self.assertTrue(results[0]['price'] == f'{self.product.price:.2f}')
        self.assertTrue(results[0]['stock'] == self.product.stock)

    def test_get_product_success(self):
        response = self.apiClient.get(self.base_url + f'{self.product.id}/')

        self.assertTrue(response.status_code == status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data['name'] == self.product.name)
        self.assertTrue(data['price'] == f'{self.product.price:.2f}')
        self.assertTrue(data['stock'] == self.product.stock)

    def test_get_product_404(self):
        response = self.apiClient.get(self.base_url + f'{self.product.id + 1}/')

        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND)

    def test_create_product_success(self):
        response = self.apiClient.post(
            self.base_url,
            data={
                'name': 'Arroz',
                'price': 4.5,
                'stock': 100,
            },
        )

        self.assertTrue(response.status_code == status.HTTP_201_CREATED)

    def test_create_product_error_empty_data(self):
        response = self.apiClient.post(
            self.base_url,
            data={},
        )

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertTrue(data['name'] == ['This field is required.'])
        self.assertTrue(data['price'] == ['This field is required.'])
        self.assertTrue(data['stock'] == ['This field is required.'])

    def test_create_product_error_price_and_stock_invalid(self):
        response = self.apiClient.post(
            self.base_url,
            data={
                'name': 'Arroz',
                'price': 'Teste',
                'stock': 'Teste',
            },
        )

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertTrue(data['price'] == ['A valid number is required.'])
        self.assertTrue(data['stock'] == ['A valid integer is required.'])

    def test_update_product_success(self):
        response = self.apiClient.put(
            self.base_url + f'{self.product.id}/',
            data={
                'name': 'Arroz Parboilizado',
                'price': 5.0,
                'stock': 200,
            },
        )

        self.assertTrue(response.status_code == status.HTTP_200_OK)
        data = response.json()
        print(data)
        self.assertTrue(data['name'] == 'Arroz Parboilizado')
        self.assertTrue(data['price'] == '5.00')
        self.assertTrue(data['stock'] == 200)

    def test_update_product_error_empty_data(self):
        response = self.apiClient.put(
            self.base_url + f'{self.product.id}/',
            data={},
        )

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertTrue(data['name'] == ['This field is required.'])
        self.assertTrue(data['price'] == ['This field is required.'])
        self.assertTrue(data['stock'] == ['This field is required.'])

    def test_update_product_error_invalid_data(self):
        response = self.apiClient.put(
            self.base_url + f'{self.product.id}/',
            data={
                'name': 'Arroz',
                'price': 'Teste',
                'stock': 'Teste',
            },
        )

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertTrue(data['price'] == ['A valid number is required.'])
        self.assertTrue(data['stock'] == ['A valid integer is required.'])
