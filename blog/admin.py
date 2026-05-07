from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    actions = ['make_published', 'make_draft']

    def make_published(self, request, queryset):
        queryset.update(status='published')
    make_published.short_description = "Belgilangan postlarni Published qilish"

    def make_draft(self, request, queryset):
        queryset.update(status='draft')
    make_draft.short_description = "Belgilangan postlarni Draft qilish"
