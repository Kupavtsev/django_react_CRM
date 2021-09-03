from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Account

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'last_login', 'date_joined')
    list_display_links = ('username', 'email', 'date_joined')
    search_fields = ('username', 'email')

class CustomersAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'email', 'phone', 'telegram_id', 'createdAt')
    list_display_links = ('last_name', 'email', 'telegram_id')
    search_fields = ('email', 'phone')

admin.site.register(Customer, CustomersAdmin)
admin.site.register(Account, AccountAdmin)
# admin.site.register(Account, UserAdmin)