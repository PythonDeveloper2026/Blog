from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    content = RichTextField()
    summary = models.CharField(max_length=150, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    
    tags = TaggableManager(blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # handle unique slug
            original_slug = self.slug
            queryset = Post.objects.filter(slug=original_slug)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            counter = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                queryset = Post.objects.filter(slug=self.slug)
                if self.pk:
                    queryset = queryset.exclude(pk=self.pk)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', args=[self.slug])

    def total_likes(self):
        return self.likes.count()

    def get_reading_time(self):
        # A simple method: ~200 words per minute
        from django.utils.html import strip_tags
        word_count = len(strip_tags(self.content).split())
        minutes = max(1, word_count // 200)
        return minutes

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
