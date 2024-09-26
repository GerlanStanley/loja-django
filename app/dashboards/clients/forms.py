from django.forms import ModelForm, CharField, EmailField, TextInput

from app.clients.models import Client


class ClientForm(ModelForm):
    name = CharField(
        label='Nome',
        max_length=100,
        widget=TextInput(attrs={'placeholder': 'Informe o nome', 'class': 'form-control'})
    )
    email = EmailField(
        label='E-mail',
        max_length=100,
        widget=TextInput(attrs={'placeholder': 'Informe o e-mail', 'class': 'form-control'})
    )

    class Meta:
        model = Client
        fields = ['name', 'email']

    def save_client(self):
        client = Client(
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
        )
        client.save()
