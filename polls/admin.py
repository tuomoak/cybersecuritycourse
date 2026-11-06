
from django.contrib import admin

from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created')
    list_filter = ['created']
    search_fields = ['title', 'content', 'author__username']

admin.site.register(Post, PostAdmin)
