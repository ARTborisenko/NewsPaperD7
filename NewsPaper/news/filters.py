from django_filters import FilterSet
from .models import Post


class PostsFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'author': ['exact'],
            'heading': ['icontains'],
            'add_time': ['gte']
        }