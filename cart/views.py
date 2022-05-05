from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse

from .cart import Cart
from store.models import Product
#from . cart import Cart
def cart_summary (request):
    return render (request, 'cart/cart_summary.html') 


def cart_add(request):
    
    cart = Cart(request)
    
    # get session 
    
    if request.POST.get('action')== 'post':
        # check the type of request from ajax
        product_id = int(request.POST.get('productid'))
        # get product id from ajax wheb button is clicked
        product  = get_object_or_404(Product,id=product_id)
        # get id from Product table and save check if they match with product_id
        cart.add(product=product)
        # create add fuction to add data in the session, this funtion is passed to cart.py (add function)
        
        response = JsonResponse({'dfgdfg':'dfgdf',})
       
        return response