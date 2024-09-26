from django.urls import path

from app.dashboards.clients.views import ClientsListView, CreateClient, ClientDetailView
from app.dashboards.home.views import HomeView
from app.dashboards.orders.views import OrdersListView, CreateOrder, OrderDetailView
from app.dashboards.products.views import ProductsListView, ProductDetailView, CreateProduct

app_name = "dashboard"

urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home",
    ),

    path(
        "clients/",
        ClientsListView.as_view(),
        name="clients-list",
    ),
    path(
        "clients/create/",
        CreateClient.as_view(),
        name="client-form",
    ),
    path(
        "clients/<int:pk>/",
        ClientDetailView.as_view(),
        name="client-detail",
    ),

    path(
        "products/",
        ProductsListView.as_view(),
        name="products-list",
    ),
    path(
        "products/create/",
        CreateProduct.as_view(),
        name="product-form",
    ),
    path(
        "products/<int:pk>/",
        ProductDetailView.as_view(),
        name="product-detail",
    ),

    path(
        "orders/",
        OrdersListView.as_view(),
        name="orders-list",
    ),
    path(
        "orders/create/",
        CreateOrder.as_view(),
        name="order-form",
    ),
    path(
        "orders/<int:pk>/",
        OrderDetailView.as_view(),
        name="order-detail",
    ),
]
