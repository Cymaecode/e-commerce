from PIL.Image import item
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from store.models import Product
from . cart import Cart
from . forms import CartAddProductForm

# serves the cart add page to the user
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id = product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product = product,
            quantity = cd['quantity'],
            override_quantity = cd['override'],
            size = request.POST.get('size'),
            color = request.POST.get('color'),
        )
    # htmx response
    if request.htmx:
        cart_item_count = sum(item["quantity"] for item in cart)
        return JsonResponse({
            "cart_count": cart_item_count,
            "message": f"{product.name} added to cart!",
        })

    return redirect("cart:cart_detail")

# serves the cart remove page to the user
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    # return redirect('cart:cart_detail')
    return render(request, 'cart/cart_remove.html')

# serves the cart detail page to the user
def cart_detail(request):
    # cart = Cart(request)
    #
    # # update quantity
    # for item in cart:
    #     item["update_quantity_form"] = CartAddProductForm(
    #         initial={
    #             "quantity": item['quantity'],
    #             "override": True
    #         }
    #     )

    # return render(request, 'cart/detail.html', {'cart': cart})
    return render(request, 'cart/cart_detail.html')
