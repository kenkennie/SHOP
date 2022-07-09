from django.contrib import admin
from .models import PostCategory, BlogPost, Comment
from blog import models
from mptt.admin import MPTTModelAdmin


# Register your models here.


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time',)
    list_filter = ('name', 'created_time',)
    list_display_links = ('name',)
    prepopulated_fields = {'category_slug': ('name',), }


admin.site.register(PostCategory, PostCategoryAdmin)


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    list_filter = ('title', 'created')
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ('title', 'post_description', 'author',)


admin.site.register(BlogPost, BlogPostAdmin)


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'publish_date','status')
    list_filter = ('publish_date','status',)
    search_fields = ('name',)
    list_editable = ('status',)
