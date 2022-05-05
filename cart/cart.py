class Cart():
    '''A base cart class, providing some default bahaviours that can be inheriter or
    be overirded as necessary'''
    def __init__(self, request):
        self.sess = request.session
        # Request.session - is treated as dictonary  django requests session method
        # by default Session table has session id and cookie
        # self.sess is a variablr to request.session
        crt =  self.sess.get('skey')
        # if user is new, he doesn't have a session
        # if he has, the they will have a cookie in the browser(with has a id) - which will be referenced by session name(skey)   # if there is data, the it will be stored in crt       
        # skey is the session name (you can create many sessions, so its importance to name sessions)
        if 'skey' not in request.session:
            # check if user has a sesson
            basket= self.sess['skey']={}
            # if there is no session, create and save in basket
        self.basket = crt
        # get the created session and save in crt


    def add(self, product):
        '''
            add data to session
        '''
        product_id=product.id
        # get product.id(from product) and save to product_id