from django.contrib import admin
from .models import Post, Comment  
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'created_on', 'category')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'subtitle', 'content']
    list_filter = ('created_on', 'author')
    summernote_fields = ('body')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'body', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'email', 'body', 'post')
