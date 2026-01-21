from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from . models import Category, Product
# TODO: from cart.forms import CartAddProductForm

# Create your views here.

# TODO: product_list view
def product_list(request):
    return render(request, "store/product_list.html")

# TODO: product_details view