from .models import Cart, CartItem


def cart_count(request):
    cart_count = 0
    try:
        cart = Cart.objects.filter(cart_id=request.session.session_key)
        if cart.exists():
            cart_items = CartItem.objects.filter(cart=cart[0], is_active=True)
            for cart_item in cart_items:
                cart_count += cart_item.quantity
    except Exception:
        cart_count = 0
    return {'cart_count': cart_count}
