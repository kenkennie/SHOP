from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [

    path('', views.cart_summary, name='cart_summary'),
    path('cart_add/', views.cart_add, name='cart_add'),
    path('cart_summary', views.cart_summary, name='cart_summary'),

]
