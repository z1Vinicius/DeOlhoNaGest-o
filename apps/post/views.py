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

# class ProfileData(APIView):
#     [IsAuthenticated]
#     def get(self, request, *args, **kwargs):    
#         return Response('Usuário não está autenticado', status= status.HTTP_401_UNAUTHORIZED)