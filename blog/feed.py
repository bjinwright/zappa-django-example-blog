from django.conf import settings
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords, truncatewords_html, safe

from .models import Post

class LatestEntriesFeed(Feed):
    title = "Jinwright"
    link = "http://www.jinwright.net/"
    description = "A blog about web development, serverless computing, "\
                  "easier scalability, and using AWS Cloud to bring down "\
                  "DevOps cost and time."

    def items(self):
        return Post.objects().filter({'active': True})

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body,80)

    def item_pubdate(self, item):
        return item.date_added
