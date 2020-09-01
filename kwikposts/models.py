from django.db import models
from django.conf import settings
from django.utils.text import slugify


# Create your models here.


class KwikPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='kwikposts_created', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, blank=True)
    featured_image = models.ImageField(upload_to='user_posts/images/%Y/%m/%d/')
    post_body = models.TextField(max_length=140, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    post_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='kwiktalk_posts_liked', blank=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.post_body

    def number_of_likes(self):
        return self.post_likes.all().count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.post_body)
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(KwikPost, on_delete=models.CASCADE)
    user_comment = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(KwikPost, on_delete=models.CASCADE)
    values = models.CharField(choices=LIKE_CHOICES, max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
