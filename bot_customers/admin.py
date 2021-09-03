from django.contrib import admin
from .models import UserTelegram

class TelegaAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'email', 'phone', 'city', 'registred')
    list_display_links = ('last_name', 'email', 'city')
    search_fields = ('email', 'phone')

admin.site.register(UserTelegram, TelegaAdmin)