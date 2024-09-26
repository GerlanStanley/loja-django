from django.contrib import admin

from app.orders.models import Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    raw_id_fields = ['product']


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['client', 'datetime']
    ordering = ['-id']
    inlines = [OrderProductInline]
    raw_id_fields = ['client']


admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Order, OrderAdmin)
