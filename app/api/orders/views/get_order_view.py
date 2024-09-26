from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from app.api.orders.serializers.order_complete_serializer import OrderCompleteSerializer
from app.orders.models import Order


class GetOrderView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCompleteSerializer
    permission_classes = [IsAuthenticated]

    class Meta:
        model = Order

    def retrieve(self, request, *args, **kwargs):
        return super(GetOrderView, self).retrieve(request, *args, **kwargs)

