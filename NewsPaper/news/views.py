from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostsFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    template_name = 'all_news.html'
    context_object_name = 'all_news'
    queryset = Post.objects.order_by('-add_time')


class SearchNews(NewsList):
    template_name = 'search.html'
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
    template_name = 'post_detail.html'
    queryset = Post.objects.all()
    context_object_name = 'news'


class PostCreateView(CreateView):
    template_name = 'post_create.html'
    form_class = PostForm
    success_url = '/news/'


class PostUpdateView(UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm
    queryset = Post.objects.all()
    success_url = '/news/'

    def gt_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    context_object_name = 'news'
    success_url = '/news/'
