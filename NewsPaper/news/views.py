from django.views.generic import ListView, DetailView  # импортируем класс получения деталей объекта
from .models import Post


class NewsList(ListView):
    model = Post
    template_name = 'all_news.html'
    context_object_name = 'all_news'
    queryset = Post.objects.order_by('-add_time')


class News(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
