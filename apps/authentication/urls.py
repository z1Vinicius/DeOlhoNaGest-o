from django.urls import path
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView)
from .views import ProfileData

urlpatterns = [
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/auth/profile/', ProfileData.as_view(), name='profile_data'),
    
    
    # path("<str:room_name>/", room, name="room"),

] 