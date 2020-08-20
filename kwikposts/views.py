from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import KwikTalkPostForm

# Create your views here.


@login_required
def kwiktalk_post_create(request):
    if request.method == 'POST':
        post_form = KwikTalkPostForm(data=request.POST)
        if post_form.is_valid():
            cd = KwikTalkPostForm.cleaned_data
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Post successfully added')
        else:
            messages.error(request, 'Error adding a post')