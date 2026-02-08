from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from . models import Category, Product
from cart.forms import CartAddProductForm

# Create your views here.

# serves the home page to the user
def home(request):
    return render(request, "store/home.html")

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'shop/product/detail.html', context)