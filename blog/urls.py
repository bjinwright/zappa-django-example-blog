from django.conf.urls import url

from .views import PostView,PostListView,CategoryView,PostViewInactive
from .feed import LatestEntriesFeed

urlpatterns = (
    url(r'^$',PostListView.as_view(), name='post-list'),
    url(r'^feed/$', LatestEntriesFeed(), name='feed'),
    url(r'^category/(?P<slug>[-\w]+)/$',CategoryView.as_view(), name='category-list'),
    url(r'^admin/(?P<slug>[-\w]+)/$',PostViewInactive.as_view(), name='post-detail-inactive'),
    url(r'^(?P<slug>[-\w]+)/$',PostView.as_view(), name='post-detail'),


)