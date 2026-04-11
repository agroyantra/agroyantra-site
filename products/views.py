from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product
from categories.models import Category


def product_list(request):
    products = Product.objects.filter(is_available=True).order_by('-is_featured', 'product_name')
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    availability = request.GET.get('availability')
    if availability:
        products = products.filter(availability=availability)

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    categories = Category.objects.all()

    context = {
        'products': paged_products,
        'product_count': products.count(),
        'categories': categories,
        'selected_category': selected_category,
        'selected_availability': availability,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(
        Product, category__slug=category_slug, slug=product_slug, is_available=True
    )
    related = Product.objects.filter(
        category=product.category, is_available=True
    ).exclude(id=product.id)[:4]
    context = {
        'product': product,
        'related_products': related,
    }
    return render(request, 'products/product_detail.html', context)


def search(request):
    keyword = request.GET.get('keyword', '').strip()
    products = Product.objects.none()
    if keyword:
        products = Product.objects.filter(is_available=True).filter(
            Q(product_name__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(brand__icontains=keyword) |
            Q(model_number__icontains=keyword) |
            Q(category__category_name__icontains=keyword)
        ).distinct()
    context = {
        'products': products,
        'product_count': products.count(),
        'keyword': keyword,
    }
    return render(request, 'products/search.html', context)
