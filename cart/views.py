from PIL.Image import item
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import override
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from store.models import Product
from . cart import Cart
from . forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id = product_id)

    # Get from data
    form = CartAddProductForm(request.POST)
    quantity = int(request.POST.get("quantity", 1))
    size = request.POST.get("size", "")
    color = request.POST.get("color", "")
    override = request.POST.get("override", "false") == "true"

    # Add to cart
    cart.add(
        product = product,
        quantity = quantity,
        override_quantity = override,
        size = size,
        color = color,
    )

    # htmx response
    if request.htmx:
        cart_count = sum(item["quantity"] for item in cart)
        return JsonResponse({
            "cart_count": cart_count,
            "message": f"{product.name} added to cart!",
        })

    return redirect("cart:cart_detail")

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id = product_id)

    # Get size and color if provided
    size = request.POST.get("size", "")
    color = request.POST.get("color", "")

    cart.remove(product, size = size, color = color)

    # htmx response - return updated cart HTML
    if request.htmx:
        return cart_detail(request) # Return the full cart vew

    return redirect("cart:cart_detail")

def cart_detail(request):
    cart = Cart(request)

    # prepare cart items for template
    cart_items = []
    for item in cart:
        cart_items.append(item)

    context = {
        "cart": cart,
        "cart_items": cart_items,
        "total_price": cart.get_total_price(),
    }

    # htmx response for partial update
    if request.htmx:
        return render(request, "cart/partials/_cart_items.html", context)

    return render(request, "cart/cart_detail.html", context)
