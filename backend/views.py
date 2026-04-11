from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum, Count, Q
import datetime
from orders.models import Order, OrderProduct, Payment
from products.models import Product
from accounts.models import Account
from categories.models import Category
from gallery.models import GalleryAlbum, GalleryImage


def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access denied. Staff only.')
        return redirect('home')
    wrapper.__name__ = view_func.__name__
    return login_required(wrapper, login_url='login')


@staff_required
def dashboard(request):
    orders = Order.objects.filter(is_ordered=True).order_by('-created_at')
    total_orders = orders.count()
    new_orders = orders.filter(status='New').count()
    dispatched = orders.filter(status='Dispatched').count()
    total_revenue = orders.filter(status='Delivered').aggregate(t=Sum('order_total'))['t'] or 0
    total_products = Product.objects.count()
    low_stock = Product.objects.filter(availability='in_stock', stock__lte=5, stock__gt=0).count()
    total_customers = Account.objects.filter(role='customer').count()
    context = {
        'orders': orders[:10],
        'total_orders': total_orders,
        'new_orders': new_orders,
        'dispatched': dispatched,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'low_stock': low_stock,
        'total_customers': total_customers,
    }
    return render(request, 'backend/dashboard.html', context)


@staff_required
def order_list(request):
    orders = Order.objects.filter(is_ordered=True).order_by('-created_at')
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    search = request.GET.get('q', '')
    if search:
        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone__icontains=search)
        )
    context = {
        'orders': orders,
        'status_filter': status_filter,
        'search': search,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'backend/order_list.html', context)


@staff_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    order_items = order.items.all()
    staff_list = Account.objects.filter(is_staff=True)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_status':
            status = request.POST.get('status')
            if status in dict(Order.STATUS_CHOICES):
                order.status = status
                if status == 'Dispatched':
                    order.dispatch_date = datetime.date.today()
                elif status == 'Delivered':
                    order.delivery_date = datetime.date.today()
                    if order.payment:
                        order.payment.status = 'Collected'
                        order.payment.save()
                order.save()
                messages.success(request, f'Order #{order_number} status → {status}')
        elif action == 'update_delivery':
            order.delivery_note = request.POST.get('delivery_note', '')
            order.vehicle_number = request.POST.get('vehicle_number', '')
            order.driver_name = request.POST.get('driver_name', '')
            order.driver_phone = request.POST.get('driver_phone', '')
            assigned_id = request.POST.get('assigned_to')
            if assigned_id:
                order.assigned_to_id = assigned_id
            order.save()
            messages.success(request, 'Delivery details updated.')
        return redirect('backend_order_detail', order_number=order_number)

    context = {
        'order': order,
        'order_items': order_items,
        'subtotal': order.order_total - order.tax - order.delivery_charge,
        'staff_list': staff_list,
    }
    return render(request, 'backend/order_detail.html', context)


@staff_required
def delivery_document(request, order_number):
    """Printable delivery order document."""
    order = get_object_or_404(Order, order_number=order_number)
    order_items = order.items.all()
    context = {
        'order': order,
        'order_items': order_items,
        'subtotal': order.order_total - order.tax - order.delivery_charge,
        'print_date': datetime.date.today(),
    }
    return render(request, 'backend/delivery_document.html', context)


@staff_required
def product_list(request):
    products = Product.objects.all().select_related('category').order_by('-created_date')
    context = {'products': products}
    return render(request, 'backend/product_list.html', context)


@staff_required
def staff_list(request):
    staff = Account.objects.filter(Q(is_staff=True) | Q(role='staff')).order_by('first_name')
    context = {'staff': staff}
    return render(request, 'backend/staff_list.html', context)


@staff_required
def customer_list(request):
    customers = Account.objects.filter(role='customer').order_by('-date_joined')
    context = {'customers': customers}
    return render(request, 'backend/customer_list.html', context)
