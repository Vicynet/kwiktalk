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
from django.views.generic import UpdateView, DeleteView, ListView
from django.urls import reverse_lazy


# Create your views here.

@login_required
class FriendPost(ListView):
    model = KwikPost

    def get_queryset(self):
        return KwikPost.objects.filter(user__exact=self.request.user.friends)


@login_required
def list_create_post(request):
    added_post = KwikPost.objects.all()
    user = request.user
    all_user_post = KwikPost.objects.filter(user=user).all().count()
    all_user_likes = Like.objects.filter(user=user).all().count()
    post_by_friends = KwikPost.objects.filter(friend=user.friends).all()

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
        'friend_post': post_by_friends,
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


class DeletePost(DeleteView):
    model = KwikPost
    template_name = 'delete_post.html'
    success_url = reverse_lazy('kwikposts:post_feed')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post_delete_obj = KwikPost.objects.get(pk=pk)
        if not post_delete_obj.user == self.request.user:
            messages.warning(self.request, "You need to be the author of the post to delete it!")
        return post_delete_obj


class UpdatePost(UpdateView):
    form_class = KwikTalkPostForm
    model = KwikPost
    template_name = 'update_post.html'
    success_url = reverse_lazy('kwikposts:post_feed')

    # def form_valid(self, form):
    #     user = Profile.objects.get(user=self.request.user)
    #     if form.instance.user == user:
    #         return super().form_valid(form)
    #     else:
    #         form.add_error(None, "You need to be the author of the post to update it!")
    #         return super().form_invalid(form)

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post_update_obj = KwikPost.objects.get(pk=pk)
        if not post_update_obj.user == self.request.user:
            messages.warning(self.request, "You need to be the author of the post to update it!")
        return post_update_obj
