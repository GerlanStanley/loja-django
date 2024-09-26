from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.api.products.serializers.product_serializer import ProductSerializer
from app.products.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
