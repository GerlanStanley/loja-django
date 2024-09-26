from django.urls import path

from app.api.orders.views.create_order_view import CreateOrderView
from app.api.orders.views.get_all_orders_view import GetAllOrdersView
from app.api.orders.views.get_order_view import GetOrderView

urlpatterns = [
    path('create/', CreateOrderView.as_view()),
    path('<int:pk>/', GetOrderView.as_view()),
    path('', GetAllOrdersView.as_view()),
]