from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

# serves the home page to the user
def home(request):
    return render(request, 'store/home.html')
