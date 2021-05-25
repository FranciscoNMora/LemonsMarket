import uuid as uuid
from django.contrib.auth.models import User
from django.db import models


class StockManager(models.Manager):
    def get_by_natural_key(self, isin: str) -> 'Stock':
        return self.get(isin=isin)


class Stock(models.Model):
    isin = models.CharField(max_length=12, primary_key=True, db_index=True)
    name = models.CharField(max_length=200, unique=True, db_index=True)

    objects = StockManager()

    def __str__(self):
        return self.name


class OrderManager(models.Manager):
    def get_by_natural_key(self, uuid: str) -> 'Order':
        return self.get(uuid=uuid)


class Order(models.Model):
    """
    Order
    """
    stock = models.ForeignKey(Stock, related_name='orders', on_delete=models.CASCADE, db_index=True)
    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, db_index=True)
    limit_price = models.FloatField(null=True, blank=True)
    side = models.BooleanField()  #buy=True, sell=False
    valid_until = models.DateTimeField(db_index=True)
    quantity = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now=True, db_index=True)

    objects = StockManager()

    def __str__(self):
        return f'{"buy" if self.side else "sell"} {self.quantity} x {self.stock.name}'
