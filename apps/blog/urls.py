from django.urls import path
from apps.blog.views import BlogView,BlogDetailView

urlpatterns = [
    path('', BlogView.as_view(), name="blog"),
    path('<slug:slug>/', BlogDetailView.as_view(), name="post_detail"),
]