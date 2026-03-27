from django.shortcuts import render

# Contact Us view
def contact_us(request):
    return render(request, 'help_page/contact_us.html')

# FAQs view
def faqs(request):
    return render(request, 'help_page/faqs.html')

# Return view
def returns(request):
    return render(request, 'help_page/returns.html')

# Shipping view
def shipping(request):
    return render(request, 'help_page/shipping.html')
