from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView

from app.dashboards.orders.forms import OrderProductFormSet, OrderForm
from app.orders.models import Order, OrderProduct


class OrdersListView(ListView):
    template_name = 'dashboard/pages/orders/list.html'
    context_object_name = 'orders'
    model = Order
    queryset = Order.objects.all().order_by('-id')
    paginate_by = 2


class OrderDetailView(DetailView):
    template_name = 'dashboard/pages/orders/details.html'
    model = Order


class CreateOrder(TemplateView):
    template_name = 'dashboard/pages/orders/form.html'

    def get(self, *args, **kwargs):
        form = OrderForm()
        order_product_formset = OrderProductFormSet(queryset=OrderProduct.objects.none())
        return self.render_to_response({
            'form': form,
            'order_product_formset': order_product_formset
        })

    def post(self, *args, **kwargs):
        form = OrderForm(self.request.POST)
        order_product_formset = OrderProductFormSet(data=self.request.POST)

        if form.is_valid() and order_product_formset.is_valid():
            try:
                form.save_order(order_product_formset)
                return redirect(reverse_lazy('dashboard:orders-list'))
            except ValidationError:
                ...

        return self.render_to_response({
            'form': form,
            'order_product_formset': order_product_formset,
        })
