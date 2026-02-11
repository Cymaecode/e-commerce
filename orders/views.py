from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from cart.cart import Cart
from . models import Order, OrderItem
from . forms import OrderCreateForm
from store.models import Product


def order_create(request):
    cart = Cart(request)

    # Redirect if cart is empty
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Create order
            order = form.save(commit=False)

            # Add user if authenticated
            if request.user.is_authenticated:
                order.user = request.user

            order.save()

            # Create order items from cart
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    size=item.get('size', ''),
                    color=item.get('color', ''),
                )

            # Clear the cart
            cart.clear()

            # HTMX response
            if request.htmx:
                return render(request, 'orders/partials/_order_success.html', {'order': order})

            messages.success(request, f'Order #{order.id} created successfully!')
            return redirect('orders:order_detail', order_id=order.id)
        else:
            # Form is invalid - show errors
            context = {
                'cart': cart,
                'cart_items': list(cart),  # Convert to list for template
                'form': form,
            }
            return render(request, 'orders/order_create.html', context)

    # GET request - show empty form
    else:
        # Pre-fill form for authenticated users
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        form = OrderCreateForm(initial=initial_data)

        # Prepare cart items for template
        cart_items = []
        for item in cart:
            cart_items.append(item)

        context = {
            'cart': cart,
            'cart_items': cart_items,
            'form': form,
        }
        return render(request, 'orders/order_create.html', context)

# def order_create(request):
#     cart = Cart(request)
#
#     # Redirect if cart is empty
#     if len(cart) == 0:
#         messages.warning(request, "Your cart is empty.")
#         return redirect("cart:cart_detail")
#
#     if request.method == "POST":
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             # create order
#             order = form.save(commit = False)
#
#             # add user of authenticated
#             if request.user.is_authenticated:
#                 order.user = request.user
#                 order.email = request.user.email
#
#             order.save()
#
#             # create order items from cart
#             for item in cart:
#                 OrderItem.objects.create(
#                     order = order,
#                     product = item["product"],
#                     price = item["price"],
#                     quantity = item["quantity"],
#                     size = item.get("size", ""),
#                     color = item.get("color", ""),
#                 )
#
#             # clear the cart
#             cart.clear()
#
#             # htmx response
#             if request.htmx:
#                 return render(request, "orders/partials/_order_success.html", {"order": order})
#
#             messages.success(request, f"Order #{order.id} created successfully.")
#             return redirect("orders:order_detail", order_id = order.id)
#
#         else:
#
#             # Pre-fill form for authenticated users
#             initial_data = {}
#             if request.user.is_authenticated:
#                 initial_data = {
#                     "first_name": request.user.first_name,
#                     "last_name": request.user.last_name,
#                     "email": request.user.email,
#                 }
#             form = OrderCreateForm(initial = initial_data)
#
#         context = {
#             "cart": cart,
#             "form": form,
#         }
#         return render(request, "orders/order_create.html", context)


@login_required
def order_list(request):
    orders = Order.objects.filter(user = request.user)
    return render(request, "orders/order_list.html", {"orders": orders})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id = order_id)

    # check permission
    if not request.user.is_staff and (order.user and order.user != request.user):
        messages.error(request, "You are not authorized to view this order.")
        return redirect("store:home")

    return render(request, "orders/order_detail.html", {"order": order})

