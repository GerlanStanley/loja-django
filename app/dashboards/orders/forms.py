from typing import List

from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import ModelForm, ModelChoiceField, Select, modelformset_factory, IntegerField, TextInput

from app.clients.models import Client
from app.orders.models import Order, OrderProduct
from app.products.models import Product


class OrderProductForm(ModelForm):
    product = ModelChoiceField(
        label='Produto',
        required=True,
        queryset=Product.objects.all(),
        widget=Select(attrs={
            'placeholder': 'Informe o produto',
            'class': 'form-control',
        })
    )
    quantity = IntegerField(
        label='Quantidade',
        required=True,
        widget=TextInput(attrs={
            'placeholder': 'Informe a quantidade',
            'class': 'form-control',
        })
    )

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']


OrderProductFormSet = modelformset_factory(
    OrderProduct,
    form=OrderProductForm,
    fields=['product', 'quantity'],
    extra=1,
)


class OrderForm(ModelForm):
    client = ModelChoiceField(
        label='Cliente',
        queryset=Client.objects.all(),
        widget=Select(attrs={
            'placeholder': 'Informe o cliente',
            'class': 'form-control',
        })
    )

    class Meta:
        model = Order
        fields = ['client']

    @transaction.atomic
    def save_order(self, formset: OrderProductFormSet):
        if formset.total_form_count() <= 0:
            raise ValidationError('Informe os itens')

        print(self.cleaned_data['client'])
        client = Client.objects.get(pk=self.cleaned_data['client'].id)

        order = Order(
            client=client,
        )

        order.save()

        items: List[OrderProduct] = []
        for form in formset:
            if not "product" in form.cleaned_data:
                form.add_error('product', 'Informe o produto')
                raise ValidationError('Informe o produto')
            if not "quantity" in form.cleaned_data:
                raise ValidationError('Informe a quantidade')

            items.append(OrderProduct(
                order=order,
                product=form.cleaned_data['product'],
                quantity=form.cleaned_data['quantity'],
            ))

        OrderProduct.objects.bulk_create(items)
