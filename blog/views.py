from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from taggit.models import Tag
from users.models import Notification

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(status='published')
        
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])
            
        sort_by = self.request.GET.get('sort', 'newest')
        if sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort_by == 'a-z':
            queryset = queryset.order_by('title')
        elif sort_by == 'z-a':
            queryset = queryset.order_by('-title')
        else:
            queryset = queryset.order_by('-created_at')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            context['tag'] = get_object_or_404(Tag, slug=tag_slug)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(status='published') | Q(author=self.request.user))
        return Post.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Like logic
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['liked'] = liked
        
        # Comment form
        context['comment_form'] = CommentForm()
        
        # Related posts based on tags
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids, status='published').exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created_at')[:4]
        context['similar_posts'] = similar_posts
        
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            
            # Create notification for post author
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    notification_type='comment',
                    post=post,
                    text=f'{request.user.username} sizning "{post.title}" postingizga izoh qoldirdi.'
                )
            return redirect('post-detail', slug=post.slug)
        return self.get(request, *args, **kwargs)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        
        # Notify followers about the new post
        post = self.object
        if post.status == 'published':
            followers = self.request.user.profile.followers.all()
            notifications = []
            for follower in followers:
                notifications.append(
                    Notification(
                        recipient=follower,
                        sender=self.request.user,
                        notification_type='post',
                        post=post,
                        text=f'{self.request.user.username} yangi post yozdi: "{post.title}"'
                    )
                )
            Notification.objects.bulk_create(notifications)
            
        return response

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog-home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

class SearchListView(ListView):
    model = Post
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Post.objects.filter(
                (Q(title__icontains=query) | Q(content__icontains=query)),
                status='published'
            ).order_by('-created_at')
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[slug]))

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'slug': self.object.post.slug})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'slug': self.object.post.slug})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

