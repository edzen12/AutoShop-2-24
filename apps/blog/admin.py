from django.contrib import admin
from apps.blog.models import Tag, Post


admin.site.register(Tag)
admin.site.register(Post)
