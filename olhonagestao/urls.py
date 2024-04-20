from apps.authentication.urls import urlpatterns as loginUrls
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import  path


urlpatterns = [
    path('admin/', admin.site.urls),
] + loginUrls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
