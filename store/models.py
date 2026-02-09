from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 200, db_index = True)
    slug = models.SlugField(max_length = 200, db_index = True)

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product_list_by_category", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name = "products", on_delete = models.CASCADE)
    name = models.CharField(max_length = 200, db_index = True)
    slug = models.SlugField(max_length = 200, db_index = True)
    image = models.ImageField(upload_to = "products/%Y/%m/%d", blank = True)
    description = models.TextField(blank = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    available = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    stock = models.PositiveIntegerField(default = 0)

    rating = models.DecimalField(max_digits = 3, decimal_places = 2, default = 0.0)
    review_count = models.IntegerField(default = 0)
    sizes = models.JSONField(default = list, blank = True)
    colors = models.JSONField(default = list, blank = True)
    gallery = models.JSONField(default = list, blank = True)

    # Gender
    GENDER_CHOICES = (
        ("Men", "Men"),
        ("Women", "Women"),
        ("Unisex", "Unisex"),
    )
    gender = models.CharField(max_length = 10, choices = GENDER_CHOICES, default = "Unisex")
    original_price = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, blank = True)
    is_new = models.BooleanField(default = False)

    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.id, self.slug])

    def in_stock(self):
        return self.stock > 0

    def get_discount(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    def get_discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0