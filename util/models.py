import docb

from django.conf import settings


class Session(docb.Document):
    session_key = docb.SlugProperty()
    data = docb.CharProperty()
    created = docb.DateTimeProperty(auto_now_add=True)

    class Meta:
        use_db = 'dynamodb'
        handler = settings.DOCB_HANDLER
