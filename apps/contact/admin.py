from django.contrib import admin
from apps.contact.models import (
    ContactPage, ContactRequest)


admin.site.register(ContactPage)
admin.site.register(ContactRequest)