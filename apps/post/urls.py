from django.urls import path
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView)
from .views import UserPosts, RecentFeed, UpdateFeed

urlpatterns = [
    path('api/posts/user/', UserPosts.as_view(), name='get_user_posts'),
    path('api/posts/feed/', RecentFeed.as_view(), name='get_feed_posts'),
    path('api/posts/feed/update', UpdateFeed.as_view(), name='update_feed_posts'),
] 