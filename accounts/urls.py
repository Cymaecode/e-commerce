from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path("accounts/register", views.register_view, name="register_view"),
    path("accounts/login", views.login_view, name="login_view"),
    path("accounts/logout", views.logout_view, name="logout"),
    path("accounts/profile", views.profile_view, name="profile_view"),
]