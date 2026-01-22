from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm


def signup_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'تم إنشاء حسابك بنجاح!')
            return redirect('core:home')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'مرحباً {user.username}!')
                next_url = request.GET.get('next', 'core:home')
                return redirect(next_url)
            else:
                messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'تم تسجيل خروجك بنجاح.')
    return redirect('users:login')


@login_required
def profile_view(request):
    """Display user profile."""
    return render(request, 'users/profile.html')
