from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostsFilter
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def subscribe_category(request, pk):
    if request.user not in Category.objects.get(pk=pk).subscribers.all():
        Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect(f'/news/')

@login_required
def unsubscribe_category(request, pk):
    if request.user in Category.objects.get(pk=pk).subscribers.all():
        Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect(f'/news/')


class NewsList(ListView):
    model = Post
    template_name = 'news/all_news.html'
    context_object_name = 'all_news'
    queryset = Post.objects.order_by('-add_time')


class SearchNews(NewsList):
    template_name = 'news/search.html'
    context_object_name = 'search_news'
    paginate_by = 10

    def get_filter(self):
        return PostsFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
        }


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_signed'] = self.request.user
        return context


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.create_post', )
    template_name = 'news/post_create.html'
    form_class = PostForm
    success_url = '/news/'


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.update_post',)
    template_name = 'news/post_create.html'
    form_class = PostForm
    queryset = Post.objects.all()
    success_url = '/news/'

    def gt_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    context_object_name = 'news'
    success_url = '/news/'


