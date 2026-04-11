from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('product_name', 'category', 'availability', 'show_price', 'price', 'stock', 'is_available', 'is_featured')
    list_editable = ('availability', 'show_price', 'price', 'stock', 'is_available', 'is_featured')
    list_filter   = ('category', 'availability', 'is_available', 'is_featured', 'show_price')
    search_fields = ('product_name', 'brand', 'model_number', 'description')
    prepopulated_fields = {'slug': ('product_name',)}
    readonly_fields = ('created_date', 'modified_date')

    fieldsets = (
        ('Basic Information', {
            'fields': ('product_name', 'slug', 'category', 'brand', 'model_number',
                       'short_description', 'description', 'specifications', 'images')
        }),
        ('Pricing', {
            'fields': ('show_price', 'price', 'discount_price')
        }),
        ('Stock & Availability', {
            'fields': ('availability', 'stock', 'unit', 'min_order_quantity', 'overseas_lead_time')
        }),
        ('Visibility', {
            'fields': ('is_available', 'is_featured')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_date', 'modified_date'),
            'classes': ('collapse',)
        }),
    )
