
from .models import Category

def categories(request):
    #to make categories view to be available on all pages #set up on settings.py
    return{
        'categories' :  Category.objects.all()

    }
    #return categories,{'categories':categories}
