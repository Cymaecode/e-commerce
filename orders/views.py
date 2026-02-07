from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import Order, OrderItem
from . forms import OrderCreateForm
from cart.cart import Cart

# Create your views here.

# serves the order create page to the user
@login_required
def order_create(request):
    if request.method == 'POST':
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.paid = True  # In real app, this would be after payment
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            cart.clear()
            messages.success(request, 'Order placed successfully!')
            return redirect('orders:order_detail', order_id = order.id)
    else:
        form = OrderCreateForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'address': request.user.address,
        })

    # return render(request, 'orders/order/create.html', {
    #     'cart': cart,
    #     'form': form,
    # })
    return render(request, 'orders/order_create.html', {
        'cart': cart,
        'form': form,
    })

# serves the order list page to the user
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    # return render(request, 'orders/order/list.html', {'orders': orders})
    return render(request, 'orders/order_list.html')

# serves the order detail page to the user
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id = order_id, user=request.user)
    # return render(request, 'orders/order/detail.html', {'order': order})
    return render(request, 'orders/order_detail.html')
