from django.contrib import admin

from app.clients.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


admin.site.register(Client, ClientAdmin)
