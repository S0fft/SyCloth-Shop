from collections.abc import Iterable

import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key: str = settings.STRIPE_SECRET


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
    image = models.ImageField(upload_to='products_images', null=True, blank=True)
    stripe_product_price_id: int = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name: str = 'product'
        verbose_name_plural: str = 'products'

    def __str__(self) -> str:
        return f'Product: {self.name} | Category: {self.category.name}'

    def save(self,
             force_insert: bool = ...,
             force_update: bool = ...,
             using: str | None = ...,
             update_fields: Iterable[str] | None = ...) -> None:

        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']

        super(Product, self).save(force_insert=False, force_update=False, using=None, )

    def create_stripe_product_price(self) -> float:
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency='usd')

        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    def total_sum(self) -> int:
        return sum(basket.sum() for basket in self)

    def total_quantity(self) -> int:
        return sum(basket.quantity for basket in self)

    def stripe_products(self) -> list:
        line_items: list = []

        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)

        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product: str = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity: int = models.PositiveSmallIntegerField(default=0)
    created_timestamp: int = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self) -> str:
        return f'Basket for {self.user.username} | Product: {self.product.name}'

    def sum(self) -> int:
        return self.product.price * self.quantity

    def de_json(self) -> dict[str, str | int | float]:
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        return basket_item

    @classmethod
    def create_or_update(cls, product_id: int, user):
        baskets: list = Basket.objects.filter(user=user, product_id=product_id)

        if not baskets.exists():
            obj = Basket.objects.create(user=user, product_id=product_id, quantity=1)
            is_created: bool = True

            return obj, is_created
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            is_created: bool = False

            return basket, is_created
