from model_bakery import baker
from rest_framework import status

from app.clients.models import Client
from app.core.tests import CommonTestCase
from app.orders.models import Order, OrderProduct
from app.products.models import Product


class OrderTestCase(CommonTestCase):
    def setUp(self):
        super().setUp()
        self.client = baker.make(Client)

        self.product1 = Product(id=1, name='Produto 1', price=10.5, stock=10)
        self.product1.save()
        self.product2 = Product(id=2, name='Produto 2', price=5.0, stock=20)
        self.product2.save()

        self.order = baker.make(Order)
        self.order.client = self.client
        self.order.save()

        self.orderProduct1 = OrderProduct(order=self.order, product=self.product1, quantity=10)
        self.orderProduct1.save()
        self.orderProduct2 = OrderProduct(order=self.order, product=self.product2, quantity=5)
        self.orderProduct2.save()

        self.base_url = '/api/v1/orders/'

    def test_get_all_orders_success(self):
        response = self.apiClient.get(self.base_url)

        self.assertTrue(response.status_code == status.HTTP_200_OK)
        data = response.json()
        self.assertTrue('results' in data)
        results = data['results']
        self.assertTrue(isinstance(results, list))
        self.assertTrue(len(results))
        self.assertTrue(results[0]['client']['id'] == self.order.client.id)

    def test_get_order_success(self):
        response = self.apiClient.get(self.base_url + f'{self.order.id}/')

        self.assertTrue(response.status_code == status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data['client']['id'] == self.order.client.id)
        self.assertTrue(data['items'][0]['product']['id'] == self.product1.id)
        self.assertTrue(data['items'][1]['product']['id'] == self.product2.id)

    def test_create_order_success(self):
        response = self.apiClient.post(
            self.base_url + 'create/',
            format='json',
            data={
                "client": self.client.id,
                "items": [
                    {
                        "product": 1,
                        "quantity": 2
                    },
                    {
                        "product": 2,
                        "quantity": 5
                    }
                ],
            },
        )

        self.assertTrue(response.status_code == status.HTTP_201_CREATED)
        product1_aux = Product.objects.get(id=self.product1.id)
        product2_aux = Product.objects.get(id=self.product2.id)
        self.assertTrue(product1_aux.stock == self.product1.stock - 2)
        self.assertTrue(product2_aux.stock == self.product2.stock - 5)

    def test_create_order_error_empty_data(self):
        response = self.apiClient.post(
            self.base_url + 'create/',
            format='json',
            data={},
        )

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertTrue(data['client'] == ['This field is required.'])
        self.assertTrue(data['items'] == ['This field is required.'])

    def test_create_order_error_client_invalid(self):
        response = self.apiClient.post(
            self.base_url + 'create/',
            format='json',
            data={
                "client": self.client.id + 1,
                "items": [
                    {
                        "product": 1,
                        "quantity": 2
                    },
                    {
                        "product": 2,
                        "quantity": 5
                    }
                ],
            },
        )

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertTrue(data['client'] == ['O cliente não existe'])

    def test_create_order_error_items_empty(self):
        response = self.apiClient.post(
            self.base_url + 'create/',
            format='json',
            data={
                "client": self.client.id,
                "items": [],
            },
        )

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertTrue(data['items'] == ['Informe os itens'])

    def test_create_order_error_product_invalid(self):
        response = self.apiClient.post(
            self.base_url + 'create/',
            format='json',
            data={
                "client": self.client.id,
                "items": [
                    {
                        "product": 100,
                        "quantity": 11
                    },
                    {
                        "product": 2,
                        "quantity": 21
                    }
                ],
            },
        )

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertTrue(data['items'][0]['product'] == ['O produto não existe'])

    def test_create_order_error_items_stock_limit(self):
        response = self.apiClient.post(
            self.base_url + 'create/',
            format='json',
            data={
                "client": self.client.id,
                "items": [
                    {
                        "product": 1,
                        "quantity": 11
                    },
                    {
                        "product": 2,
                        "quantity": 21
                    }
                ],
            },
        )

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertTrue(
            data['items'][0]['product[0]'] == ['Não existe quantidade em estoque disponível para o produto 0'])

    def test_create_order_error_items_stock_limit_2(self):
        response = self.apiClient.post(
            self.base_url + 'create/',
            format='json',
            data={
                "client": self.client.id,
                "items": [
                    {
                        "product": 1,
                        "quantity": 5
                    },
                    {
                        "product": 2,
                        "quantity": 21
                    }
                ],
            },
        )

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertTrue(
            data['items'][0]['product[1]'] == ['Não existe quantidade em estoque disponível para o produto 1'])
