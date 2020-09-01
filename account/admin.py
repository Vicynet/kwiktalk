from django.contrib import admin
from .models import Profile, Relationship


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'date_of_birth', 'display_picture', 'bio', 'gender', 'slug']


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'created_at']

