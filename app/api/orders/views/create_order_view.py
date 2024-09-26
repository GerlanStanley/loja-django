from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api.orders.serializers.create_order_serializer import CreateOrderSerializer
from app.clients.models import Client
from app.orders.models import Order, OrderProduct
from app.products.models import Product


class CreateOrderView(APIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        data = serializer.data

        try:
            client = Client.objects.get(id=data['client'])
        except Client.DoesNotExist:
            raise ValidationError(
                {
                    'client': [
                        'O cliente não existe'
                    ]
                }
            )

        order = Order(client=client)
        order.save()

        if not data['items']:
            raise ValidationError(
                {
                    'items': [
                        'Informe os itens'
                    ]
                }
            )

        try:
            for index, item in enumerate(data['items']):
                product = Product.objects.get(id=item.get('product'))

                quantity = item.get('quantity')

                if product.stock < quantity:
                    raise ValidationError(
                        {
                            'items': [
                                {
                                    f'product[{index}]': [
                                        f'Não existe quantidade em estoque disponível para o produto {index}'
                                    ]
                                }
                            ]
                        }
                    )

                OrderProduct(order=order, product=product, quantity=quantity).save()
                product.stock -= quantity
                product.save()

        except Product.DoesNotExist:
            raise ValidationError(
                {
                    'items': [
                        {
                            'product': [
                                'O produto não existe'
                            ]
                        }
                    ]
                }
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
