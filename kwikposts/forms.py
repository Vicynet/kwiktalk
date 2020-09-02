from django import forms
from .models import KwikPost, Comment
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class KwikTalkPostForm(forms.ModelForm):
    class Meta:
        model = KwikPost
        fields = ('featured_image', 'post_body')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user_comment',)

    # def clean_featured_image(self):
    #     featured_image = self.cleaned_data['featured_image']
    #     valid_image_extensions = ['jpg', 'jpeg', 'png', 'gif']
    #     extension = featured_image.rsplit('.', 1)[1].lower()
    #     if extension not in valid_image_extensions:
    #         raise forms.ValidationError('The chosen image does not match a valid image extension.')
    #     return featured_image

    # def save(self, force_insert=False, force_update=False, commit=True):
    #     featured_image = super().save(commit=False)
    #     post_image = self.cleaned_data['featured_image']
    #     name = slugify(featured_image.post_body)
    #     extension = post_image.rsplit('.', 1)[1].lower()
    #     featured_image_name = f'{name}.{extension}'

        # response = request.

