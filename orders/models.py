from django.db import models

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

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Order №{self.id}. For: {self.first_name} {self.last_name}"
