from decimal import Decimal

from store.models import Product


class Cart():
    '''A base cart class, providing some default bahaviours that can be inheriter or
    be overirded as necessary'''

    def __init__(self, request):
        self.sess = request.session
        # Request.session - is treated as dictonary  django requests session method
        # by default Session table has session id and cookie
        # self.sess is a variablr to request.session
        crt = self.sess.get('skey')
        # if user is new, he doesn't have a session
        # if he has, the they will have a cookie in the browser(with has a id) - which will be referenced by session name(skey)   # if there is data, the it will be stored in crt       
        # skey is the session name (you can create many sessions, so its importance to name sessions)
        if 'skey' not in request.session:
            # check if user has a sesson
            crt = self.sess['skey'] = {}
            # if there is no session, create and save in basket
        self.basket = crt
        # get the created session and save in crt

    def add(self, product, Qty):
        '''
            add data to session 
            product,product_Qty is passed from view
        '''
        product_id = product.id
        # get product.id(from product) and save to product_id
        if product_id not in self.basket:
            # check if product id exists in session.crt
            self.basket[product_id] = {'price': int(product.price), 'Qty': int(Qty)}
            # if it doen't exist, add price
        self.sess.modified = True

    def __iter__(self):
        '''
        collect the product_id in the session data to query the database and 
        return products
        '''
        product_ids = self.basket.keys()
        # collect product id that are in session and 
        products = Product.objects.filter(id__in=product_ids)
        # get product from db, and filter products id in table with the ones ids in session
        cart = self.basket.copy()
        # copy data from sesssion data
        for prdct in products:
            # loop through data from database
            # each product that is looped it is saved in variable product
            cart[str(prdct.id)]['product'] = prdct

            # add more data
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = Decimal(item['price'] * item['Qty'])
            yield item

    def __len__(self):
        '''
        get the basket data and count the quantity of all products
        '''
        return sum(prdct['Qty'] for prdct in self.basket.values())
        # iterate over the product quantity,calculate values of all products tha have quantity

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['Qty'] for item in self.basket.values())

        """
            Get total price
        """

    def delete(self, productId):
        ''' delete product from session data'''
        product_id = str(productId)
        print(product_id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def save(self):
        self.sess.modified = True
