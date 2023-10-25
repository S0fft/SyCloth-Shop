from django.contrib import admin

from products.admin import BasketAdmin
from users.models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display: list[str] = ['username', 'email', 'image']
    inlines = [BasketAdmin]


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display: list[str] = ['code', 'user', 'expiration']
    fields: list[str] = ['code', 'user', 'expiration', 'created']
    readonly_fields: list[str] = ['created']
