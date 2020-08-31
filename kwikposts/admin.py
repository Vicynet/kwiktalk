from django.contrib import admin
from .models import KwikPost

# Register your models here.


@admin.register(KwikPost)
class KwikPostAdmin(admin.ModelAdmin):
    list_display = ['user', 'featured_image', 'slug', 'post_body', 'created_at']
    list_filter = ['created_at']
    prepopulated_fields = {'slug': ('post_body',)[:20]}
