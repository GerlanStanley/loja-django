from rest_framework import serializers


class CreateOrderProductSerializer(serializers.Serializer):
    product = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True, min_value=1)

    class Meta:
        fields = ['product', 'quantity']


class CreateOrderSerializer(serializers.Serializer):
    client = serializers.IntegerField(required=True)
    items = CreateOrderProductSerializer(required=True, many=True)

    class Meta:
        fields = ['client', 'datetime', 'items']
        read_only_fields = ['datetime']
