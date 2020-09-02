from django.contrib import admin
from .models import KwikPost, Comment, Like

# Register your models here.


@admin.register(KwikPost)
class KwikPostAdmin(admin.ModelAdmin):
    list_display = ['user', 'featured_image', 'slug', 'post_body', 'created_at']
    list_filter = ['created_at']
    prepopulated_fields = {'slug': ('post_body',)[:20]}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'user_comment', 'created_at']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'values', 'created_at']

