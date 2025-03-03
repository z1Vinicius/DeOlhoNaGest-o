from django.urls import path, re_path
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView)
from .views import UserPosts, RecentFeed, UpdateFeed, PostCreateAPIView, LikeUnlikePostAPIView, UpdatePostStatusAPIView


urlpatterns = [
    path('api/posts/user/', UserPosts.as_view(), name='get_user_posts'),
    path('api/posts/feed/', RecentFeed.as_view(), name='get_feed_posts'),
    path('api/posts/feed/update', UpdateFeed.as_view(), name='update_feed_posts'),
    path('api/posts/create', PostCreateAPIView.as_view(), name='update_create_posts'),
    re_path(r'^api/posts/(?P<post_id>[0-9a-fA-F]{32})/like/$', LikeUnlikePostAPIView.as_view(), name='like_post'),
    re_path(r'^api/posts/(?P<post_id>[0-9a-fA-F]{32})/unlike/$', LikeUnlikePostAPIView.as_view(), name='unlike_post'),
    re_path(r'^api/posts/(?P<post_id>[0-9a-fA-F]{32})/delete/$', UpdatePostStatusAPIView.as_view(), name='update_post_status'),
] 