from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from orders.models import Order


@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')[:5]
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    context = {
        'orders': orders,
        'orders_count': Order.objects.filter(user=request.user, is_ordered=True).count(),
        'user_profile': user_profile,
    }
    return render(request, 'profile/dashboard.html', context)


@login_required(login_url='login')
def edit_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.save()

        user_profile.address_line_1 = request.POST.get('address_line_1', '')
        user_profile.address_line_2 = request.POST.get('address_line_2', '')
        user_profile.city = request.POST.get('city', '')
        user_profile.state = request.POST.get('state', '')
        user_profile.country = request.POST.get('country', 'Nepal')
        if 'profile_picture' in request.FILES:
            user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('dashboard')

    context = {'user_profile': user_profile}
    return render(request, 'profile/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user
        if user.check_password(current_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully. Please login again.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Current password is incorrect.')

    return render(request, 'profile/change_password.html')
