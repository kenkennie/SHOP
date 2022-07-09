from .models import PostCategory


def blog_categories(request):
    # make categories to be available in all pages
    return {
        'blog_categories': PostCategory.objects.all()
    }
