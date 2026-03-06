from django.views.generic import ListView, DetailView
from apps.blog.models import Category, Tag, Post


class BlogView(ListView):
    model = Post
    template_name = 'pages/blog.html'
    context_object_name = 'posts'
    paginate_by = 6
    ordering = ['-created_at']


class BlogDetailView(DetailView):
    model = Post
    template_name = 'pages/blog-detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'