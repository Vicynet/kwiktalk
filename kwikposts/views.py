from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import KwikTalkPostForm
from django.shortcuts import get_object_or_404
from .models import KwikPost
from account.models import Profile
from django.contrib.auth.models import User
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView
from django.conf import settings


# Create your views here.


@login_required
def list_create_post(request):
    added_post = KwikPost.objects.all()

    if request.method == "POST":
        # form is sent
        post_form = KwikTalkPostForm(request.POST, request.FILES)

        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            post_form.save()

            post_form = KwikTalkPostForm()
            messages.success(request, 'Post successfully added')

        else:
            messages.error(request, 'Error adding a post')

    else:
        post_form = KwikTalkPostForm(instance=request.user)

    # post_form = KwikTalkPostForm(instance=request.user)

    context = {
        'added_post': added_post,
        'post_form': post_form,
    }
    #
    return render(request, 'feed.html', context)
    # return render(request, 'feed.html', {'section': 'kwikposts', 'posts': posts})


# def list_post(request, id, slug):
#     post = get_object_or_404(KwikPost, id=id, slug=slug)
#     return render(request, 'profile/feed.html')

@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = KwikPost.objects.get(id=post_id)
            if action == 'like':
                post.post_likes.add(request.user)
            else:
                post.post_likes.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def user_post(request):
    logged_in_user_posts = KwikPost.objects.filter(user=request.user)
    return render(request, 'account/profile.html', {'post': logged_in_user_posts})

