from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path("cart/cart_add", views.cart_add, name="cart_add"),
    path("cart/cart_remove", views.cart_remove, name="cart_remove"),
    path("cart/cart_detail", views.cart_detail, name="cart_detail"),
]
