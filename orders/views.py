import datetime
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from carts.models import CartItem, Cart
from .models import Order, OrderProduct, Payment


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


@login_required(login_url='login')
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request), is_active=True)

    if cart_items.count() <= 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('product_list')

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (13 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        # Generate unique order number: date + user_id + random 4-digit suffix
        current_date = datetime.date.today().strftime('%Y%m%d')
        suffix = str(random.randint(1000, 9999))
        order_number = f'{current_date}{current_user.id}{suffix}'
        # Ensure uniqueness
        while Order.objects.filter(order_number=order_number).exists():
            suffix = str(random.randint(1000, 9999))
            order_number = f'{current_date}{current_user.id}{suffix}'

        data = Order()
        data.user = current_user
        data.first_name = request.POST.get('first_name')
        data.last_name = request.POST.get('last_name')
        data.phone = request.POST.get('phone')
        data.email = request.POST.get('email')
        data.address_line_1 = request.POST.get('address_line_1')
        data.address_line_2 = request.POST.get('address_line_2', '')
        data.city = request.POST.get('city')
        data.state = request.POST.get('state')
        data.country = request.POST.get('country', 'Nepal')
        data.order_note = request.POST.get('order_note', '')
        data.order_total = grand_total
        data.tax = tax
        data.ip = request.META.get('REMOTE_ADDR')
        data.order_number = order_number
        data.save()

        # Create Payment record (COD - pending until delivery)
        payment = Payment(
            user=current_user,
            payment_id=f'COD-{order_number}',
            payment_method='COD',
            amount_paid=grand_total,
            status='Pending',
        )
        payment.save()

        data.payment = payment
        data.is_ordered = True
        data.save()

        # Move cart items to order
        for item in cart_items:
            order_product = OrderProduct()
            order_product.order = data
            order_product.payment = payment
            order_product.user = current_user
            order_product.product = item.product
            order_product.quantity = item.quantity
            order_product.product_price = item.product.price
            order_product.ordered = True
            order_product.save()

            # Reduce stock
            product = item.product
            product.stock -= item.quantity
            product.save()

        # Clear cart
        CartItem.objects.filter(cart__cart_id=_cart_id(request)).delete()

        messages.success(request, f'Your order #{order_number} has been placed! We will confirm shortly.')
        return redirect('order_complete', order_number=order_number)

    # GET request — redirect back to checkout
    return redirect('checkout')


@login_required(login_url='login')
def order_complete(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    order_products = OrderProduct.objects.filter(order=order)
    context = {
        'order': order,
        'order_products': order_products,
        'subtotal': order.order_total - order.tax,
    }
    return render(request, 'orders/order_complete.html', context)


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'orders/my_orders.html', context)


@login_required(login_url='login')
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    order_products = OrderProduct.objects.filter(order=order)
    context = {
        'order': order,
        'order_products': order_products,
        'subtotal': order.order_total - order.tax,
    }
    return render(request, 'orders/order_detail.html', context)
