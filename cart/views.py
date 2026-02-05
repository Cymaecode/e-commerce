from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

# serves the cart add page to the user
def cart_add(request):
    return render(request, 'cart/cart_add.html')

# serves the cart remove page to the user
def cart_remove(request):
    return render(request, 'cart/cart_remove.html')

# serves the cart detail page to the user
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')
