from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'update')
    search_fields = ('slug', 'body')
    list_filter = ('update',)
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)
