from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render

from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from kwikposts.models import KwikPost, Comment, Like
from django.db.models import Q


# Create your models here.
# class Contact(models.Model):
#     user_from = models.ForeignKey('auth.User', related_name='relationship_from_set', on_delete=models.CASCADE)
#     user_to = models.ForeignKey('auth.User', related_name='relationship_to_set', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#
#     class Meta:
#         ordering = ('-created_at',)
#
#     def __str__(self):
#         return f'{self.user_from} follows {self.user_to}'


class ProfileManager(models.Manager):
    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        friend_relation = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        print(friend_relation)

        accepted = set([])
        for rel in friend_relation:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print(accepted)

        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        return available


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    display_picture = models.ImageField(default='default_avatar.png', upload_to='users/%Y/%m/%d/', blank=True)
    bio = models.CharField(max_length=140, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)

    # friends = models.ManyToManyField(User, through=Contact, blank=True, related_name='friends', symmetrical=False)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # user_model = get_user_model()
    # user_model.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers',
    #                                                             symmetrical=False))

    def get_friends(self):
        return self.friends.all()

    def get_friends_number(self):
        return self.friends.all().count()

    def get_likes_given(self):
        likes = self.Like.all().count()
        total_liked = 0
        for item in likes:
            if item.values == 'Like':
                total_liked += 1
        return total_liked

    def __str__(self):
        return f"Profile for user {self.user.username}-{self.created_at.strftime('%d-%m-%Y')}"

    def save(self, *args, **kwargs):
        ex = False
        if self.user.first_name and self.user.last_name:
            to_slug = slugify(str(self.user.first_name) + " " + str(self.user.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        new_invitation = Relationship.objects.filter(receiver=receiver, status='send')
        return new_invitation


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.sender} follows {self.receiver}-{self.status}"
