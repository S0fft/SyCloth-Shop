from django.db import models

from products.models import Basket
from users.models import User


class Order(models.Model):
    CREATED: int = 0
    PAID: int = 1
    ON_WAY: int = 2
    DELIVERED: int = 3
    STATUSES: list[list] = (
        (CREATED, 'Created'),
        (PAID, 'Paid'),
        (ON_WAY, 'On way'),
        (DELIVERED, 'Delivered'),
    )

    first_name: str = models.CharField(max_length=64)
    last_name: str = models.CharField(max_length=64)
    email: str = models.EmailField(max_length=256)
    address: str = models.CharField(max_length=256)
    basket_history: dict = models.JSONField(default=dict)
    created: int = models.DateTimeField(auto_now=True)
    status: int = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator: str = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Order №{self.id}. For: {self.first_name} {self.last_name}"

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status: str = self.PAID
        self.basket_history: dict[str, list[str] | float] = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum())
        }
        baskets.delete()
        self.save()
