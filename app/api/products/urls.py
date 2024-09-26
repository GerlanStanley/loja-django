from django.urls import path, include
from rest_framework import routers

from app.api.products.views.product_view_set import ProductViewSet

router = routers.DefaultRouter()
router.register(r'', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]