from django.shortcuts import render


def about_us(request):
    return render(request, 'about_us_farm/about.html')


def our_farm(request):
    return render(request, 'about_us_farm/our_farm.html')


def contact(request):
    return render(request, 'about_us_farm/contact.html')
