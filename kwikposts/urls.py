from django.urls import path
from . import views

app_name = 'kwikposts'

urlpatterns = [
    path('', views.kwiktalk_post_create, name='feed'),
]
