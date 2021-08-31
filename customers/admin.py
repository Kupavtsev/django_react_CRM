from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer

# Register your models here.
admin.site.register(Customer)
# admin.site.register(Account)
# admin.site.register(Account, UserAdmin)