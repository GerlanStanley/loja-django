from django.forms import ModelForm, CharField, TextInput, IntegerField, DecimalField

from app.products.models import Product


class ProductForm(ModelForm):
    name = CharField(
        label='Nome',
        max_length=100,
        widget=TextInput(attrs={'placeholder': 'Informe o nome', 'class': 'form-control'})
    )
    price = DecimalField(
        label='Preço',
        max_digits=10,
        decimal_places=2,
        widget=TextInput(attrs={'placeholder': 'Informe o preço', 'class': 'form-control'})

    )
    stock = IntegerField(
        label='Estoque',
        min_value=0,
        widget=TextInput(attrs={'placeholder': 'Informe a quantidade em estoque', 'class': 'form-control'})
    )

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']

    def save_product(self):
        product = Product(
            name=self.cleaned_data['name'],
            price=self.cleaned_data['price'],
            stock=self.cleaned_data['stock'],
        )
        product.save()
