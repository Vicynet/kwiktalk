from django.urls import path
from . import views

app_name = 'kwikposts'

urlpatterns = [
    path('', views.list_create_post, name='post_feed'),
    path('like/', views.post_like, name='like'),
    # path('/post', views.PostCreate, name='feed'),
]
