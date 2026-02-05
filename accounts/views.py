from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . forms import CustomUserCreationForm
from . models import User

# Create your views here.

# serves the register page to the user
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect("home")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

# serves the login page to the user
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        user = authenticate(request, username=user.username if user else None, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect("home")
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login_view.html')

# serves the register page to the user
@login_required
def profile_view(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.phone = request.POST.get('phone', '')
        user.address = request.POST.get('address', '')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile_view.html')

# serves the logout page to the user
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out")
    # return render(request, 'accounts/logout_view.html')
    return redirect("home")