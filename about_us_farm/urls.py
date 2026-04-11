from django.urls import path
from . import views

urlpatterns = [
    path('', views.about_us, name='about_us'),
    path('our-farm/', views.our_farm, name='our_farm'),
    path('contact/', views.contact, name='contact'),
]
