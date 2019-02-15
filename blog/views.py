from braces.views import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse
from django.views.generic import DetailView, ListView, FormView
from django_warrant.views.mixins import GetUserMixin, TokenMixin
from docb.exceptions import QueryError

from blog.forms import PostForm, UpdatePostForm
from .models import CATEGORIES, Post


class PostListView(ListView):
    template_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return self.model.objects().filter({'active': True}, sort_attr='date_added', sort_reverse=True)


class CategoryView(PostListView):
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        try:
            kwargs['category'] = CATEGORIES.get_category(self.kwargs['slug'])
        except KeyError:
            raise Http404
        return super(CategoryView, self).get_context_data(**kwargs)

    def get_queryset(self):
        return self.model.objects().filter({'active': True, 'category': self.kwargs['slug']},
                                           sort_attr='date_added', sort_reverse=True)


class PostView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_object(self, queryset=None):
        try:
            return self.model.objects().get({'slug': self.kwargs['slug'], 'active': True})
        except self.model.DoesNotExist:
            raise Http404


class PostViewInactive(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_object(self, queryset=None):
        try:
            return self.model.objects().get({'slug': self.kwargs['slug']})
        except self.model.DoesNotExist:
            raise Http404


#######################
# Admin Views         #
#######################

class AdminPostListView(LoginRequiredMixin, TokenMixin, GetUserMixin, ListView):
    template_name = 'admin/list.html'
    model = Post

    def get_queryset(self):
        return self.model.objects().all(sort_attr='date_added', sort_reverse=True)


class PostFormView(LoginRequiredMixin, TokenMixin, GetUserMixin, FormView):
    action = ''

    def get_context_data(self, **kwargs):
        kwargs = super(PostFormView, self).get_context_data(**kwargs)
        kwargs['action'] = self.action
        return kwargs

    def get_success_url(self):
        return reverse('admin-post-list')


class CreatePostView(PostFormView):
    template_name = 'admin/form.html'
    form_class = PostForm
    action = 'Create Post'

    def form_valid(self, form):
        form.save()
        return super(CreatePostView, self).form_valid(form)


class UpdatePostView(PostFormView):
    template_name = 'admin/form.html'
    form_class = UpdatePostForm

    @property
    def action(self):
        return 'Update Post: {}'.format(self.get_object().title)

    def get_object(self):
        try:
            return self.object
        except AttributeError:
            try:
                self.object = Post.objects().get({'slug':self.kwargs['slug']})
            except QueryError:
                raise Http404
            return self.object

    def get_initial(self):
        return self.get_object()._data

    def form_valid(self, form):
        form.save(self.get_object())
        return super(UpdatePostView, self).form_valid(form)




