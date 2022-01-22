from django.urls import path
from .views import AuthorUpdateView, upgrade_me

urlpatterns = [
    path('author/<int:pk>', AuthorUpdateView.as_view(), name='author_update'),
    path('author/upgrade/', upgrade_me, name='upgrade'),
]