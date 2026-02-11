from PIL.Image import item
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from store.models import Product

class Order(models.Model):
    # user information will be null for guest
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = "orders",
    )

    email = models.EmailField()

    # Shipping information
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    address = models.CharField(max_length = 250)
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    zip_code = models.CharField(max_length = 20)
    country = models.CharField(max_length = 100, default = "Country Name")

    # order detials
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    paid = models.BooleanField(default = False)

    # payment information simple
    payment_method = models.CharField(max_length = 50, default = "Credit Card")
    transaction_id = models.CharField(max_length = 100, blank = True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Order {self.id}"

    def get_tool_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name = "items",
        on_delete = models.CASCADE,
    )

    product = models.ForeignKey(
        Product,
        related_name = "order_items",
        on_delete = models.PROTECT,
    )

    price = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        validators = [MinValueValidator(Decimal("0.01"))]
    )

    quantity = models.PositiveIntegerField(default = 1)
    size = models.CharField(max_length = 10, blank = True)
    color = models.CharField(max_length = 20, blank = True)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

