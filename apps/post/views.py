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
from rest_framework.permissions import IsAuthenticated

from apps.authentication.models import Profile
from .serializers import PostSerializer
from .models import Post

class UserPosts(APIView):
    [IsAuthenticated]
    def get(self, request, *args, **kwargs):
      user = Profile.getByRequest(request)
      if not(user):
        return Response('Usuário não encontrado', status= status.HTTP_401_UNAUTHORIZED)
      query = Post.getAllPosts(user).prefetch_related('created_by', 'created_by__user', 'postmedia_set')
      serializer = PostSerializer(query, many = True)
      return Response(serializer.data)
    
class RecentFeed(APIView):
    [IsAuthenticated]
    def get(self, request, *args, **kwargs):
      user = Profile.getByRequest(request)
      query = Post.getRecentPosts().prefetch_related('created_by', 'created_by__user', 'postmedia_set', 'likes')
      serializer = PostSerializer(query, many = True, context={'profile': user})
      return Response(serializer.data)

