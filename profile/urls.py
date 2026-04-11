from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
]
