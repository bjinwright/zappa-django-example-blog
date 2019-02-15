from django import forms
from ckeditor.fields import RichTextFormField

from blog.models import CATEGORIES, Post


class PostForm(forms.Form):
    title = forms.CharField(required=True)
    slug = forms.SlugField(required=True)
    description = forms.CharField(max_length=200)
    category = forms.ChoiceField(choices=CATEGORIES.django_choices)
    keywords = forms.CharField()
    body = RichTextFormField(required=True)
    active = forms.BooleanField()

    def save(self):
        p = Post(**self.cleaned_data)
        p.save()


class UpdatePostForm(forms.Form):
    title = forms.CharField(required=True)
    description = forms.CharField(max_length=200)
    category = forms.ChoiceField(choices=CATEGORIES.django_choices)
    keywords = forms.CharField()
    body = RichTextFormField(required=True)
    active = forms.BooleanField()

    def save(self, instance):
        instance._data.update(self.cleaned_data)
        instance.save()