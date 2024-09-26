from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('v1/clients/', include('app.api.clients.urls')),
    path('v1/products/', include('app.api.products.urls')),
    path('v1/orders/', include('app.api.orders.urls')),
    path('v1/auth/', obtain_auth_token, name='api_token_auth'),
]
