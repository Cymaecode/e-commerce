from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email',
            'address', 'city', 'state',
            'zip_code', 'country',
            'payment_method'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-300',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-300',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-300',
                'placeholder': 'Email'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-300',
                'placeholder': 'Address',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-300',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-300',
                'placeholder': 'State / Province'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-300',
                'placeholder': 'Zip / Postal Code'
            }),
            'country': forms.Select(attrs={
                'class': 'w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-300'
            }, choices=[
                ('Country Name', 'Country Name'),
                ('Country Name', 'Country Name'),
                ('Country Name', 'Country Name'),
                ('Country Name', 'Country Name'),
            ]),
            'payment_method': forms.Select(attrs={
                'class': 'w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-300'
            }, choices=[
                ('Credit Card', 'Credit Card'),
                ('PayPal', 'PayPal'),
                ('Bank Transfer', 'Bank Transfer'),
            ]),
        }
