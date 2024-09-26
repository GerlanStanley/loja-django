from decimal import Decimal

from rest_framework import serializers

from app.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=100, min_length=1)
    price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2, min_value=Decimal('0.00'))
    stock = serializers.IntegerField(required=True, min_value=0)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock']
        read_only_fields = ['id']
