from django.urls import path, include
from rest_framework import routers

from app.api.clients.views.client_view_set import ClientViewSet

router = routers.DefaultRouter()
router.register(r'', ClientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]