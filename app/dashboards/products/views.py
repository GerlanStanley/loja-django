from django.views.generic import ListView, FormView, DetailView

from app.dashboards.products.forms import ProductForm
from app.products.models import Product


class ProductsListView(ListView):
    template_name = 'dashboard/pages/products/list.html'
    context_object_name = 'products'
    model = Product
    queryset = Product.objects.all().order_by('name')
    paginate_by = 2


class CreateProduct(FormView):
    template_name = 'dashboard/pages/products/form.html'
    form_class = ProductForm
    success_url = "/dashboard/products/"

    def form_valid(self, form):
        form.save_product()
        return super(CreateProduct, self).form_valid(form)


class ProductDetailView(DetailView):
    template_name = 'dashboard/pages/products/details.html'
    model = Product


