from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.search, name='search'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]
