from braces.views import LoginRequiredMixin
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView,ListView
from .models import Category,Post


class PostListView(ListView):
    model = Post

    @method_decorator(cache_page(60 * 5))
    def get(self, request, *args, **kwargs):
        return super(PostListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(active=True).order_by('-id')

class CategoryView(PostListView):
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        try:
            kwargs['category'] = Category.objects.get(slug=self.kwargs['slug'])
        except Category.DoesNotExist:
            raise Http404
        return super(CategoryView, self).get_context_data(**kwargs)

    def get_queryset(self):
        qs = super(CategoryView, self).get_queryset()
        return qs.filter(categories__slug=self.kwargs['slug'])


class PostView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        try:
            return self.model.objects.get(slug=self.kwargs['slug'],active=True)
        except self.model.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(60 * 10))
    def get(self, request, *args, **kwargs):
        return super(PostView, self).get(request, *args, **kwargs)

class PostViewInactive(LoginRequiredMixin,DetailView):
    model = Post

    def get_object(self, queryset=None):
        try:
            return self.model.objects.get(slug=self.kwargs['slug'])
        except self.model.DoesNotExist:
            raise Http404
