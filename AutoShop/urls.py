from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('about/', include('apps.about.urls')),
    path('blog/', include('apps.blog.urls')),
    path('cart/', include('apps.cart.urls')),
    path('contact/', include('apps.contact.urls')),
    path('partners/', include('apps.partners.urls')),
    path('product/', include('apps.product.urls')),
    path('users/', include('apps.users.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
