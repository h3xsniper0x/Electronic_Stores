from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    """Form for user registration with email field."""
    email = forms.EmailField(
        required=True,
        label='البريد الإلكتروني',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل بريدك الإلكتروني',
            'dir': 'ltr'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'اسم المستخدم',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Arabic labels and styling
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'أدخل اسم المستخدم',
            'dir': 'ltr'
        })
        self.fields['password1'].label = 'كلمة المرور'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'أدخل كلمة المرور',
            'dir': 'ltr'
        })
        self.fields['password2'].label = 'تأكيد كلمة المرور'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'أعد إدخال كلمة المرور',
            'dir': 'ltr'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('هذا البريد الإلكتروني مسجل بالفعل')
        return email


class UserLoginForm(forms.Form):
    """Form for user login."""
    username = forms.CharField(
        label='اسم المستخدم',
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل اسم المستخدم',
            'dir': 'ltr'
        })
    )
    password = forms.CharField(
        label='كلمة المرور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل كلمة المرور',
            'dir': 'ltr'
        })
    )
