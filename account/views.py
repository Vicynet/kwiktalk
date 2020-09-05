from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.cache import cache
from django.views.generic import ListView
from django.db.models import Q

from kwikposts.views import list_create_post
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Relationship, ProfileManager
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
                    return render(request, 'account/disabled.html', context=None)
            else:
                return render(request, 'account/failed_login.html', context=None)

        next_url = cache.get('next')
        if next_url:
            cache.delete('next')
            return HttpResponseRedirect(next_url)

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
            #Profile.objects.create(user=create_new_user)
            # return Registration successful page
            return render(redirect('account:register_done'))
            # return render(request, 'account/register_done.html', {'create_new_user': create_new_user})
    else:
        user_registration_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_registration_form': user_registration_form})


def register_done(request):
    return render(request, 'account/register_done.html')


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


# @login_required
# def user_list(request):
#     users = User.objects.exclude(username=request.user).filter(is_active=True, is_staff=False)
#     return render(request, 'account/user_list.html', {'section': 'people', 'users': users})


class ProfileListView(ListView):
    model = Profile
    template_name = 'account/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        users = Profile.objects.all().exclude(user=self.request.user)
        return users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context


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


@login_required
def invitation_received_view(request):
    # user = get_object_or_404(User, username=username, is_active=True)
    user_profile = Profile.objects.get(user=request.user)
    invites = Relationship.objects.invitations_received(user_profile)
    print(invites)
    return render(request, 'account/friend-requests.html', {'friend-requests': invites})


@login_required
def invite_profiles_list_view(request):
    user = request.user
    invite_profile = ProfileManager.get_all_profiles_to_invite(sender=user)
    return render(request, 'account/find-friend.html', {'follow-friend': invite_profile})


def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relation = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('user_list')


def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relation = Relationship.objects.create(sender=sender, receiver=receiver, status='accepted')
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('user_list')


def remove_friend(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relation = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender)))
        relation.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('user_list')
