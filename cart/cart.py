from decimal import Decimal
from django.conf import settings
from store.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity = 1, override_quantity = False, size = "", color = ""):
        # create unique key with product_id, size, and color
        item_key = f"{product.id}_{size}_{color}"

        if item_key not in self.cart:
            self.cart[item_key] = {
                'quantity': 0,
                'price': str(product.price),
                "size": size,
                "color": color,
                "product_id": str(product.id),
            }

        if override_quantity:
            self.cart[item_key]['quantity'] = quantity
        else:
            self.cart[item_key]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product, size = "", color = ""):
        item_key = f"{product.id}_{size}_{color}"

        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def __iter__(self):
        # Get all product IDs from cart
        product_ids = [item["product_id"] for item in self.cart.values()]

        # Fetch all product at once for efficiency
        products = Product.objects.filter(id__in = product_ids)
        products_dict = {str(p.id): p for p in products}

        # yield cart items with product  objects
        for item_key, item in self.cart.items():
            product = products_dict.get(item["product_id"])
            if product:
                yield {
                    "product": product,
                    "quantity": item["quantity"],
                    "price": Decimal(item["price"]),
                    "total_price": Decimal(item["price"]) * item["quantity"],
                    "size": item.get("size", ""),
                    "color": item.get("color", ""),
                    "item_key": item_key,
                }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
