from django.conf.urls import url


from .views import PostView, PostListView, CategoryView, PostViewInactive, CreatePostView, UpdatePostView, \
    AdminPostListView
from .feed import LatestEntriesFeed

urlpatterns = (
    url(r'^$',PostListView.as_view(), name='post-list'),
    url(r'^feed/$', LatestEntriesFeed(), name='feed'),
    url(r'^category/(?P<slug>[-\w]+)/$',CategoryView.as_view(), name='category-list'),
    # url(r'^admin/(?P<slug>[-\w]+)/$',PostViewInactive.as_view(), name='post-detail-inactive'),
    url(r'^admin/post/$', AdminPostListView.as_view(), name='admin-post-list'),
    url(r'^admin/post/create/$', CreatePostView.as_view(), name='create-post'),
    url(r'^admin/post/update/(?P<slug>[-\w]+)/$',UpdatePostView.as_view(), name='update-post'),
    url(r'^(?P<slug>[-\w]+)/$',PostView.as_view(), name='post-detail')
)