from django.db import models
from django.urls import reverse
from categories.models import Category


class Product(models.Model):
    AVAILABILITY_CHOICES = (
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('on_order', 'Available on Order'),
        ('overseas', 'Overseas / Import Order'),
        ('discontinued', 'Discontinued'),
    )

    product_name   = models.CharField(max_length=200, unique=True)
    slug           = models.SlugField(max_length=200, unique=True)
    description    = models.TextField(blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    specifications = models.TextField(blank=True, help_text='Technical specs (one per line)')
    brand          = models.CharField(max_length=100, blank=True)
    model_number   = models.CharField(max_length=100, blank=True)

    price          = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    show_price     = models.BooleanField(default=True, help_text='Uncheck to show "Contact for Price" instead')
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    images         = models.ImageField(upload_to='photos/products/', blank=True)
    stock          = models.IntegerField(default=0)
    availability   = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='in_stock')
    overseas_lead_time = models.CharField(max_length=100, blank=True, help_text='e.g. 4-6 weeks')
    min_order_quantity = models.PositiveIntegerField(default=1)
    unit           = models.CharField(max_length=50, default='unit')

    category       = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available   = models.BooleanField(default=True)
    is_featured    = models.BooleanField(default=False)

    meta_title       = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords    = models.CharField(max_length=300, blank=True)

    created_date   = models.DateTimeField(auto_now_add=True)
    modified_date  = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def get_meta_title(self):
        return self.meta_title or f'{self.product_name} | AgroYantra AgriTech'

    def get_meta_description(self):
        return self.meta_description or self.short_description or self.description[:160]

    def effective_price(self):
        return self.discount_price if self.discount_price else self.price

    def is_orderable(self):
        return self.availability in ('in_stock', 'on_order', 'overseas')

    def __str__(self):
        return self.product_name
