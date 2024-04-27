from apps.authentication.urls import urlpatterns as loginUrls
from apps.post.urls import urlpatterns as postUrls
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import  path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
] + loginUrls + postUrls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
