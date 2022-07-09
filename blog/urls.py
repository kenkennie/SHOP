from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.all_posts, name='all_posts'),
    path('<slug:blog_slug>', views.blog_details, name='blog_details'),
    # slug is the data type, blog_slug is the name of the variable to store
    path('category/<slug:c_slug>', views.blog_categories, name='blog_categories')

]
