from django.db import models
from django.conf import settings
from django.utils.text import slugify


# Create your models here.


class KwikPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='kwikposts_created', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, blank=True)
    featured_image = models.ImageField(upload_to='user_posts/images/%Y/%m/%d/')
    post_body = models.TextField(max_length=140, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    post_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='kwiktalk_posts_liked', blank=True)

    def __str__(self):
        return self.post_body

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.post_body[0:20])
        super().save(*args, **kwargs)
