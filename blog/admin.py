from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publishDate', 'featured')
    search_fields = ('title', 'author', 'category')
    list_filter = ('category', 'featured')
