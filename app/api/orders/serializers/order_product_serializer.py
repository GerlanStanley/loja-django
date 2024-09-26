from rest_framework import serializers

from app.api.products.serializers.product_serializer import ProductSerializer


class OrderProductSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        fields = ['quantity', 'product']
