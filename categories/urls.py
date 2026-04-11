from django.urls import path
from . import views

urlpatterns = [
    path('<slug:category_slug>/', views.products_by_category, name='products_by_category'),
]
