from django.shortcuts import render, get_object_or_404
from .models import Category
from products.models import Product


def products_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_available=True)
    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'products/products_by_category.html', context)
