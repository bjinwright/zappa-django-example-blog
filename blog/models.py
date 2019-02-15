from __future__ import unicode_literals

import docb
from django.urls import reverse
from django.conf import settings


class Category(object):

    categories = {
        'Python': 'python',
        'Serverless': 'serverless',
        'Personal': 'personal',
        'Django': 'django'
    }

    @property
    def choices(self):
        return self.categories

    @property
    def django_choices(self):
        return [(v, k) for k, v in self.categories.items()]

    @property
    def list(self):
        return [{'name': k, 'slug': v} for k, v in self.categories.items()]

    def get_category(self, slug):
        cat = list(filter(lambda x: slug == x['slug'], self.list))
        return cat[0]


CATEGORIES = Category()


class Post(docb.Document):
    title = docb.CharProperty(required=True)
    slug = docb.SlugProperty(required=True, unique=True)
    category = docb.SlugProperty(required=True, choices=CATEGORIES.choices)
    description = docb.CharProperty()
    keywords = docb.CharProperty()
    body = docb.CharProperty(required=True)
    date_added = docb.DateTimeProperty(auto_now_add=True)
    date_updated = docb.DateTimeProperty(auto_now=True)
    active = docb.BooleanProperty(default=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', args=[self.slug])

    class Meta:
        use_db = 'dynamodb'
        handler = settings.DOCB_HANDLER
