from django.conf import settings
from django.core.management import BaseCommand

from blog.models import Post


class Command(BaseCommand):
    help = 'Creates Dummy Data Table'

    def handle(self, *args, **kwargs):
        post_list = [
            Post(title='Who Am I?', slug='who-am-i', category='personal', description='A little bit about me',
                 keywords='bio, personal, brian, jinwright', body='Some text.', active=True),
            Post(title='How to Deploy Zappa WSGI Apps?', slug='how-to-deploy-zappa-wsgi-apps', category='serverless',
                 description='How to Guid on Zappa apps', keywords='serverless, zappa, python, wsgi, lambda',
                 body='Some text.', active=True)
        ]
        Post().bulk_save(post_list)


