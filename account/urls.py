from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('register/', views.register_user, name='register'),
    path('edit/', views.edit, name='edit'),
    # path('users/', views.user_list, name='user_list'),
    path('users/', views.ProfileListView.as_view(), name='user_list'),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('my-invites/', views.invitation_received_view, name='friend_request'),
    path('invite-friend/', views.invite_profiles_list_view, name='get_friend'),
    path('send-invites/', views.send_invitation, name='send-invites'),
    path('remove-friend/', views.remove_friend, name='remove-friend'),
    path('accept-friend/', views.accept_invitation, name='accept-friend'),
]
