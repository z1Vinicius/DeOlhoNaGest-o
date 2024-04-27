from django.urls import path
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView)
from .views import UserPosts

urlpatterns = [
    path('api/posts/user/', UserPosts.as_view(), name='get_user_posts'),
] 