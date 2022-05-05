from .cart import Cart
def cart(request):
    return{'caart': Cart(request)}
    