from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import KwikTalkPostForm, CommentForm
from django.shortcuts import get_object_or_404
from .models import KwikPost, Comment, Like
from account.models import Profile
from django.contrib.auth.models import User
import logging
from django.views.decorators.http import require_POST


# Create your views here.


@login_required
def list_create_post(request):
    added_post = KwikPost.objects.all()
    user = request.user
    all_user_post = KwikPost.objects.filter(user=user).all().count()
    all_user_likes = Like.objects.filter(user=user).all().count()

    if 'submit_p_form' in request.POST:
        # form is sent
        post_form = KwikTalkPostForm(request.POST, request.FILES)
        # comment_form = CommentForm(request.POST)

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
        # comment_form = CommentForm(instance=request.user)

    if 'submit_c_form' in request.POST:
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = KwikPost.objects.get(id=request.POST.get('post_id'))
            comment_form.save()

            comment_form = CommentForm()
            messages.success(request, 'Successful!')
        else:
            messages.error(request, 'Failed!')
    else:
        comment_form = CommentForm(instance=request.user)

    # post_form = KwikTalkPostForm(instance=request.user)

    context = {
        'added_post': added_post,
        'post_form': post_form,
        'user_comment': comment_form,
        'posts_by_user': all_user_post,
        'likes_by_user': all_user_likes,
    }
    #
    return render(request, 'feed.html', context)
    # return render(request, 'feed.html', {'section': 'kwikposts', 'posts': posts})

#
# @login_required
# def all_user_post(request):
#     user = request.user
#     post_by_user = KwikPost.objects.filter(user=user).all().count()
#
#     return render(request, 'feed.html', {'count_user_post': post_by_user})



@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = KwikPost.objects.get(id=post_id)

        print(post_obj.post_likes.all())
        if user in post_obj.post_likes.all():
            post_obj.post_likes.remove(user)
            # pass
        else:
            post_obj.post_likes.add(user)

        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.values == 'Like':
                like.values = 'Unlike'
            else:
                like.values = 'Like'
        else:
            like.values = 'Like'

        post_obj.save()
        like.save()

    return redirect('kwikposts:post_feed')


