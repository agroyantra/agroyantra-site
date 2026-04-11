from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .models import Account


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.phone_number = phone_number
            user.is_active = True  # Auto-activate for now
            user.save()

            messages.success(request, 'Registration successful! You can now login.')
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER', '/')
            try:
                from urllib.parse import parse_qs, urlparse
                query = parse_qs(urlparse(url).query)
                if 'next' in query:
                    return redirect(query['next'][0])
            except Exception:
                pass
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')
