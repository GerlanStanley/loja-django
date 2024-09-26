from rest_framework import serializers

from app.clients.models import Client


class ClientUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=100, min_length=1)

    class Meta:
        model = Client
        fields = ['id', 'name', 'email']
        read_only_fields = ['id', 'email']

