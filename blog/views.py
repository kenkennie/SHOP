from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import PostCategory, BlogPost, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import NewCommentForm


# Create your views here.


def all_posts(request):
    all_blogs = BlogPost.objects.all()

    # paginator
    paginator = Paginator(all_blogs, 2)  # 1 is the number of blogs per page
    page = request.GET.get('page')
    try:
        all_blogs = paginator.page(page)
    except PageNotAnInteger:
        all_blogs = paginator.page(1)
    except EmptyPage:
        # return to first page when you get to the last page
        all_blogs = paginator.page(paginator.num_pages)
    # request url for page

    return render(request, 'blog/blogs.html', {'all_blogs': all_blogs, "page": page})


def blog_details(request, blog_slug):
    # blog details
    # pass blog_slug from url requested,  -> check if it is  available
    blog = get_object_or_404(BlogPost, slug=blog_slug)
    # get blog details if not found return 404 error
    cmm = Comment.objects.filter(post=blog)
    # get comment
    user_comment = None

    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.blog = cmm
            user_comment.save()
            return render(request, '/' + blog.slug)
    else:
        comment_form = NewCommentForm

    return render(request, 'blog/blog_details.html',
                  {'blog': blog, 'comments': user_comment, 'comment_form': comment_form})


def blog_categories(request, c_slug):
    """ Blog categories"""
    b_categories = get_object_or_404(PostCategory, category_slug=c_slug)

    # get categories
    post = BlogPost.objects.filter(post_category=b_categories)

    # filter post by categories
    # return HttpResponse(blog_categories)

    return render(request, 'blog/blog_categories.html', {'b_categories': b_categories, 'post': post})
