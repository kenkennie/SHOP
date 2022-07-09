from django.urls import reverse

from django.db import models
from django.conf import settings
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
# from richtextfield.models import RichTextField

from ckeditor.fields import RichTextField


class PostCategory(models.Model):
    name = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length=100)
    created_time = models.DateTimeField(default=timezone.now, null=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('blog:blog_categories', args=[self.category_slug])

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200, blank=False)
    post_category = models.ManyToManyField(PostCategory, verbose_name='Category')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author", null=True)
    slug = models.SlugField(unique=True)
    featured_image = models.ImageField(upload_to='images/blog/%Y/%m/%d')
    post_description = RichTextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_details', args=[self.slug])

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    # parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField()
    status = models.BooleanField(default=True)
    publish_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['publish_date']

    def __str__(self):
        return f'Comment by {self.name} - Post - {self.post}'
