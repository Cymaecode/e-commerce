from django.urls import path
from . import views

app_name = 'help_page'

urlpatterns = [
    path("contact_us", views.contact_us, name="contact_us"),
    path("faqs", views.faqs, name="faqs"),
    path("returns", views.returns, name="returns"),
    path("shipping", views.shipping, name="shipping"),
]
