from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.api.clients.serializers.client_serializer import ClientSerializer
from app.api.clients.serializers.client_update_serializer import ClientUpdateSerializer
from app.clients.models import Client


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('id')
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'update':
            return ClientUpdateSerializer
        return ClientSerializer