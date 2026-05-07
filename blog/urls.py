from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    SearchListView,
    like_post,
    CommentUpdateView,
    CommentDeleteView
)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('blog/', PostListView.as_view(), name='blog-home-alt'),
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name='post-by-tag'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('write/', PostCreateView.as_view(), name='post-write'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<slug:slug>/like/', like_post, name='like-post'),
    path('posts/<slug:slug>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update-id'),
    path('posts/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete-id'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('search/', SearchListView.as_view(), name='search'),
    path('blog/search/', SearchListView.as_view(), name='search-alt'),
]
