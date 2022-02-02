from django.urls import path
from .views import *

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('search/', SearchNews.as_view()),
    path('subscribe/<int:pk>', subscribe_category, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe_category, name='unsubscribe'),
]