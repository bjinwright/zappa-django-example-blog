from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.urls import reverse
from redactor.fields import RedactorField

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-list',args=[self.slug])
    class Meta:
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    categories = models.ManyToManyField(Category,blank=True)
    description = models.CharField(max_length=160,blank=True,null=True)
    keywords = models.CharField(max_length=160,blank=True,null=True)
    body = RedactorField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',args=[self.slug])