from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, Group, User
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView, status
from axes.utils import reset
from django.shortcuts import render
import datetime
from apps.authentication.models import Profile
from rest_framework.permissions import IsAuthenticated

class ProfileData(APIView):
    [IsAuthenticated]
    def get(self, request, *args, **kwargs):    
        
        def userPermissions() -> list:
            if(request.user.is_superuser):
                permissionsQuery = Permission.objects.all()
            else:
                permissionsQuery = Permission.objects.filter(user=request.user)
                
            return [permission.codename for permission in permissionsQuery]
        
        isAuthenticated = request.user.is_authenticated
        if(isAuthenticated):
            return JsonResponse(
                {
                    "email": request.user.email,
                    'username': request.user.username,
                    'firstName': request.user.first_name,
                    'lastName': request.user.last_name,
                    'isAuthenticated': True,
                    "profileImage": Profile.getUserProfile(request.user.username),
                    "verified": True,
                    "assignments":  {
                        "permissions": userPermissions(),
                },
            })
        return Response('Usuário não está autenticado', status= status.HTTP_401_UNAUTHORIZED)