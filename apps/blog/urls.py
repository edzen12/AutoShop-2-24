from django.urls import path
from apps.blog.views import BlogView

urlpatterns = [
    path('', BlogView.as_view(), name="blog")
]