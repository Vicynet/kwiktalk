from django.urls import path
from . import views

app_name = 'kwikposts'

urlpatterns = [
    path('', views.list_create_post, name='post_feed'),
    path('liked/', views.like_unlike_post, name='like-post'),
    path('<pk>/delete/', views.DeletePost.as_view(), name='delete-post'),
    path('<pk>/update/', views.UpdatePost.as_view(), name='update-post'),
    # path('/post', views.PostCreate, name='feed'),
]
