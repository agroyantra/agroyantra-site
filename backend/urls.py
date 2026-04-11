from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='backend_dashboard'),
    path('orders/', views.order_list, name='backend_order_list'),
    path('orders/<str:order_number>/', views.order_detail, name='backend_order_detail'),
    path('orders/<str:order_number>/delivery-doc/', views.delivery_document, name='delivery_document'),
    path('products/', views.product_list, name='backend_product_list'),
    path('staff/', views.staff_list, name='backend_staff_list'),
    path('customers/', views.customer_list, name='backend_customer_list'),
]
