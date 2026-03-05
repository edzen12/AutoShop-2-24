from django.views.generic import TemplateView


class BlogView(TemplateView):
    template_name = 'pages/blog.html'