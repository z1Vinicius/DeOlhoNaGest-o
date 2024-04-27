from django.urls import path
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView)
from .views import ProfileData

urlpatterns = [
    # path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

] 