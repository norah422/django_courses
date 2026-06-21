from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title_ar', 'title_en', 'author', 'created_at')
    search_fields = ('title_ar', 'title_en', 'content_ar', 'content_en')
    list_filter = ('created_at', 'author')
