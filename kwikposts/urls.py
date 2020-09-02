from django.urls import path
from . import views

app_name = 'kwikposts'

urlpatterns = [
    path('', views.list_create_post, name='post_feed'),
    path('liked/', views.like_unlike_post, name='like-post'),
    # path('/post', views.PostCreate, name='feed'),
]
