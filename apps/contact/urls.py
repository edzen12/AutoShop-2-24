from django.urls import path
from apps.contact.views import ContactView


urlpatterns = [
    path('', ContactView.as_view(), name="contact")
]