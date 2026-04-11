from django.contrib import admin
from django.utils.html import format_html
from .models import Payment, Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model  = OrderProduct
    extra  = 0
    readonly_fields = ('product', 'quantity', 'product_price', 'ordered')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = ('order_number', 'full_name', 'phone', 'city', 'order_total',
                       'status', 'assigned_to', 'dispatch_date', 'is_ordered', 'created_at')
    list_filter     = ('status', 'is_ordered', 'created_at')
    list_editable   = ('status', 'assigned_to')
    search_fields   = ('order_number', 'first_name', 'last_name', 'phone', 'email')
    readonly_fields = ('order_number', 'ip', 'created_at', 'updated_at')
    inlines         = [OrderProductInline]

    fieldsets = (
        ('Order Info', {'fields': ('order_number', 'user', 'payment', 'status', 'is_ordered')}),
        ('Customer', {'fields': ('first_name', 'last_name', 'phone', 'email')}),
        ('Delivery Address', {'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'order_note')}),
        ('Financials', {'fields': ('order_total', 'tax', 'delivery_charge')}),
        ('Delivery Document', {
            'fields': ('delivery_note', 'assigned_to', 'dispatch_date', 'delivery_date',
                       'vehicle_number', 'driver_name', 'driver_phone')
        }),
        ('Meta', {'fields': ('ip', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


admin.site.register(Payment)
admin.site.register(OrderProduct)
