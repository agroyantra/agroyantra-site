from django.shortcuts import render
from products.models import Product
from categories.models import Category


def home(request):
    products = Product.objects.filter(is_available=True).order_by('-created_date')[:8]
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'landing_page/home.html', context)
