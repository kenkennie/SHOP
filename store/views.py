from math import prod
from django.shortcuts import get_object_or_404, render
# get_object_or_404 - gets data from database if its not available get 404 error

from .models import Category, Product

def index(request):
     # select from product database
     products= Product.objects.all()
     # render is used for loading the template
     return render(request,'store/home.html',{'products':products})
    

def product_details(request,p_slug): # get p_slug from url 
    product = get_object_or_404(Product,slug = p_slug ,in_stock=True)
    # select from Product where slug  = p_slug(from product name from url) and product should be inStock 
    return render(request,'product/product-details.html',{'product':product})

def category_list(request, c_slug):
    category =  get_object_or_404(Category,slug = c_slug)
    prod = Product.objects.filter(category=category)
    return render(request,'product/category.html',{'products':prod, 'category':category})
