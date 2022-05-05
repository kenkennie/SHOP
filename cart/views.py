
from django.shortcuts import render, get_object_or_404

from store.models import Product
#from . cart import Cart
def cart_summary (request):
    return render (request, 'cart/cart_summary.html') 
