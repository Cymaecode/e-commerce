from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

# serves the order create page to the user
def order_create(request):
    return render(request, 'orders/order_create.html')

# serves the order list page to the user
def order_list(request):
    return render(request, 'orders/order_list.html')

# serves the order detail page to the user
def order_detail(request):
    return render(request, 'orders/order_detail.html')
