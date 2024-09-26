from rest_framework import serializers

from app.clients.models import Client


class ClientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=100, min_length=1)
    email = serializers.EmailField(required=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'email']
        read_only_fields = ['id']

    @staticmethod
    def validate_email(value):
        if Client.objects.filter(email__exact=value).exists():
            raise serializers.ValidationError("Email already exists!")
        return value

