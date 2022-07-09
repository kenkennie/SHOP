from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='all_products'),
    path('category/<slug:c_slug>', views.category_list, name='category_list'),
    path('product/<slug:p_slug>', views.product_details, name='product_detail'),
    # path('product/<id:p_slug>',views.product_details,name='product_detail')
    # slug is the type of data - (converter)...eg id/slug/str/uuid - 
    # p_slug is the slug name(value)
]
