import uuid
from django.db import models
from accounts.models import Account
from products.models import Product


class Payment(models.Model):
    PAYMENT_METHOD = (('COD', 'Cash on Delivery'),)
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Collected', 'Collected'),
        ('Failed', 'Failed'),
    )
    user           = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id     = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='COD')
    amount_paid    = models.DecimalField(max_digits=12, decimal_places=2)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Confirmed', 'Confirmed'),
        ('Processing', 'Processing'),
        ('Dispatched', 'Dispatched'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user           = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment        = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number   = models.CharField(max_length=30, unique=True)

    # Customer info
    first_name     = models.CharField(max_length=50)
    last_name      = models.CharField(max_length=50)
    phone          = models.CharField(max_length=15)
    email          = models.EmailField(max_length=100)

    # Delivery address
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True)
    city           = models.CharField(max_length=50)
    state          = models.CharField(max_length=50)
    country        = models.CharField(max_length=50, default='Nepal')
    order_note     = models.TextField(blank=True)

    # Financials
    order_total    = models.DecimalField(max_digits=12, decimal_places=2)
    tax            = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_charge= models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Status & tracking
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    ip             = models.GenericIPAddressField(blank=True, null=True)
    is_ordered     = models.BooleanField(default=False)

    # Delivery document fields
    delivery_note  = models.CharField(max_length=200, blank=True, help_text='Internal delivery instructions')
    assigned_to    = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='assigned_orders', limit_choices_to={'is_staff': True})
    dispatch_date  = models.DateField(null=True, blank=True)
    delivery_date  = models.DateField(null=True, blank=True)
    vehicle_number = models.CharField(max_length=20, blank=True)
    driver_name    = models.CharField(max_length=100, blank=True)
    driver_phone   = models.CharField(max_length=15, blank=True)

    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        parts = [self.address_line_1]
        if self.address_line_2:
            parts.append(self.address_line_2)
        parts += [self.city, self.state, self.country]
        return ', '.join(parts)

    def __str__(self):
        return self.order_number


class OrderProduct(models.Model):
    order          = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    payment        = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user           = models.ForeignKey(Account, on_delete=models.CASCADE)
    product        = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity       = models.IntegerField()
    product_price  = models.DecimalField(max_digits=12, decimal_places=2)
    ordered        = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)

    def line_total(self):
        return self.product_price * self.quantity

    def __str__(self):
        return f'{self.product.product_name} x{self.quantity}'
