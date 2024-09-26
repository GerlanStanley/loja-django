from django.views.generic import ListView, FormView, DetailView

from app.clients.models import Client
from app.dashboards.clients.forms import ClientForm


class ClientsListView(ListView):
    template_name = 'dashboard/pages/clients/list.html'
    context_object_name = 'clients'
    model = Client
    queryset = Client.objects.all().order_by('name')
    paginate_by = 2


class CreateClient(FormView):
    template_name = 'dashboard/pages/clients/form.html'
    form_class = ClientForm
    success_url = "/dashboard/clients/"

    def form_valid(self, form):
        form.save_client()
        return super(CreateClient, self).form_valid(form)


class ClientDetailView(DetailView):
    template_name = 'dashboard/pages/clients/details.html'
    model = Client
