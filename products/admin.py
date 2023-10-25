from django.contrib import admin

from products.models import Basket, Product, ProductCategory

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display: list[str] = ['name', 'price', 'quantity', 'category']
    fields: list[str] = ['image', 'name', 'description', ('price', 'quantity'), 'category']
    search_fields: list[str] = ['name']
    ordering: list[str] = ['name']


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields: list[str] = ['product', 'quantity', 'created_timestamp']
    readonly_fields: list[str] = ['created_timestamp']
    extra: int = 0
