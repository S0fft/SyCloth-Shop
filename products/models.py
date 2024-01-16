from django.db import models

from users.models import User


class ProductCategory(models.Model):
    name: str = models.CharField(max_length=128, unique=True)
    description: str = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name: str = 'category'
        verbose_name_plural: str = 'categories'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name: str = models.CharField(max_length=256)
    description: str = models.TextField()
    price: int = models.DecimalField(max_digits=10, decimal_places=0)
    quantity: int = models.PositiveSmallIntegerField(default=0)
    category: str = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_images')
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name: str = 'product'
        verbose_name_plural: str = 'products'

    def __str__(self) -> str:
        return f'Product: {self.name} | Category: {self.category.name}'


class BasketQuerySet(models.QuerySet):
    def total_sum(self) -> int:
        return sum(basket.sum() for basket in self)

    def total_quantity(self) -> int:
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product: str = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity: int = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self) -> str:
        return f'Basket for {self.user.username} | Product: {self.product.name}'

    def sum(self) -> int:
        return self.product.price * self.quantity
