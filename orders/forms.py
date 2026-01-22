from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    """Form for checkout with customer information."""
    
    class Meta:
        model = Order
        fields = ['full_name', 'address', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسمك الكامل',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل عنوان التوصيل',
                'rows': 3,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل رقم هاتفك',
                'dir': 'ltr',
            }),
        }
