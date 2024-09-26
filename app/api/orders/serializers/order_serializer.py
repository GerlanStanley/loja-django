from rest_framework import serializers

from app.api.clients.serializers.client_serializer import ClientSerializer


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    datetime = serializers.DateTimeField(read_only=True)
    client = ClientSerializer(read_only=True)

    class Meta:
        fields = ['id', 'datetime', 'client']
