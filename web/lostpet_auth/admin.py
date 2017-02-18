from django.contrib import admin

from lostpet_auth.models import *
# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ['id', 'email', 'name', 'pet_name', 'created_on']

admin.site.register(Client, ClientAdmin)
