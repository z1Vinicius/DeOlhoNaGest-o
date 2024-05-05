from rest_framework.response import Response
from rest_framework.views import APIView, status
from axes.utils import reset
from django.shortcuts import render
import datetime
from rest_framework.permissions import IsAuthenticated

from apps.authentication.models import Profile
from .serializers import PostSerializer, UpdateFeedCategorySerializer, FeedCategorySerializer
from .models import Post, PostFeedIndex
from typing	 import TypeAlias

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

class UpdateFeed(APIView):
  [IsAuthenticated]
  def get(self, request, *args, **kwargs):
    serializer = UpdateFeedCategorySerializer(data = request.data)
    
    def checkUpdates(objectList, feedCategory, lastUpdate):
      for obj in objectList:
        if obj['feed_category'] == feedCategory:
          print(obj['last_update'].replace("T", " "), lastUpdate, obj['last_update'].replace("T", " ") == lastUpdate, str(lastUpdate))
          if obj['last_update'].replace("T", " ") == str(lastUpdate):
            return True
          return False
      return False
    
    if serializer.is_valid():
      data = serializer.data
      feed = PostFeedIndex.getRecentPostFeed().order_by('-id')
      
      for feedIndex in feed[:10]:
        print('valor', checkUpdates(data['categories'], feedIndex.index_name, feedIndex.updated_at))
      return Response("Evento recebido com sucesso!", status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)