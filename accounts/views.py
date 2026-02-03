from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

# serves the register page to the user
def register_view(request):
    return render(request, 'accounts/register.html')

# serves the login page to the user
def login_view(request):
    return render(request, 'accounts/login_view.html')

# serves the logout page to the user
def logout_view(request):
    return render(request, 'accounts/logout_view.html')

# serves the register page to the user
def profile_view(request):
    return render(request, 'accounts/profile_view.html')

