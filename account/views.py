from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.models import User

from kwikposts.views import list_create_post
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile  # Contact
from kwikposts.models import KwikPost, Comment, Like
from common.decorators import ajax_required


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return HttpResponse('Authenticated Successfully')
                    return list_create_post(request)
                    # return dashboard(request)
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register_user(request):
    if request.method == 'POST':
        user_registration_form = UserRegistrationForm(request.POST)
        if user_registration_form.is_valid():
            # Create a new user object but avoid saving it yet
            create_new_user = user_registration_form.save(commit=False)
            # Set chosen password for hashing for security reasons
            create_new_user.set_password(user_registration_form.cleaned_data['password'])
            # Save the new User object
            create_new_user.save()
            Profile.objects.create(user=create_new_user)
            # return Registration successful page
            return render(request, 'account/register_done.html', {'create_new_user': create_new_user})
    else:
        user_registration_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_registration_form': user_registration_form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True, is_staff=False)
    return render(request, 'account/user_list.html', {'section': 'people', 'users': users})


@login_required
def user_detail(request, username):
    # logged_in_user = request.user.profile
    # profile = Profile.objects.get(user=request.user)
    user = get_object_or_404(User, username=username, is_active=True)
    post = KwikPost.objects.filter(user=user)
    post_by_user = KwikPost.objects.filter(user=user).all().count()

    def get_likes_given(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.values == 'Like':
                total_liked += 1
        return total_liked

    likes_by_user = Like.objects.filter(user=user).all().count()
    return render(request, 'account/profile.html',
                  {'section': 'people', 'user': user, 'user_post': post,
                   'count_post': post_by_user, 'count_likes_by_user': get_likes_given(user)})


@login_required
def user_detail_post(request, username):
    post = KwikPost.objects.filter(User, username=username).all().count()
    return render(request, 'account/profile.html', {'section': 'people', 'count_user_post': post})
