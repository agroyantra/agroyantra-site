from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active', 'date_joined')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ('role', 'is_active', 'is_admin')
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
