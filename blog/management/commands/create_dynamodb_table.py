from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates DynamoDB Table'

    def handle(self, *args, **kwargs):
        if settings.DEBUG:
            from blog.models import Post
            Post().create_table()
            return 'Created local DynamoDB Table'

        settings.DOCB_HANDLER.build_cf_resource('bjinwright', 'bjinwright', 'dynamodb')
        return 'Created DynamoDB Table'
