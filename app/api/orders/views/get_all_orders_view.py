from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from app.api.orders.serializers.order_serializer import OrderSerializer
from app.orders.models import Order


class GetAllOrdersView(ListAPIView):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    class Meta:
        model = Order

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
