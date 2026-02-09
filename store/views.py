from re import search

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from . models import Category, Product
from cart.forms import CartAddProductForm

# Create home page view
def home(request):
    # Get featured products (new products or random selection)
    featured_products = Product.objects.filter(available = True).order_by("-created")[:8]

    # Get categories for navigation
    categories = Category.objects.all()[:4]  # Top 4 categories

    context = {
        'featured_products': featured_products,
        'categories': categories,
    }

    return render(request, "store/home.html", context)

def product_list(request, category_slug = None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available = True)

    # Get filter parameters
    gender = request.GET.get("gender", "all")
    price_max = request.GET.get("price_max")
    sort_by = request.GET.get("sort_by", "default")
    search_query = request.GET.get("q", "")
    is_new = request.GET.get("is_new")

    # Apply category filter
    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        products = products.filter(category = category)

    # Apply gender filter (you'll need to add gender field to product model)
    if gender != "all":
        products = products.filter(gender = gender)

    # Apply price filter
    if price_max:
        try:
            price_max = float(price_max)
            products = products.filter(price__lte = price_max)
        except ValueError:
            pass

    # Apply search
    if search_query:
        products = products.filter(
            Q(name__icontains = search_query) |
            Q(description__icontains = search_query)
        )

    # Apply sorting
    if sort_by == "newest":
        products = products.order_by("-created")
    elif sort_by == "price-asc":
        products = products.order_by("price")
    elif sort_by == "price-desc":
        products = products.order_by("-price")
    else:
        products = products.order_by("name")

    # Apply new product filter
    if is_new == "true":
        products = products.filter(is_new = True)

    context = {
        "category": category,
        "categories": categories,
        "products": products,
        "current_gender": gender,
        "current_price_max": price_max or 500,
        "current_sort": sort_by,
        "search_query": search_query,
    }

    # htmx partial response for dynamic updates
    if request.htmx:
        return render(request, "store/partials/_product_listing.html", context)

    return render(request, 'store/product_list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'shop/product/detail.html', context)