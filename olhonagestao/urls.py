from django.contrib import admin
from django.urls import path
from apps.authentication.urls import urlpatterns as loginUrls

urlpatterns = [
    path('admin/', admin.site.urls),
] + loginUrls
