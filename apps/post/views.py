from rest_framework.response import Response
from rest_framework.views import APIView, status
from axes.utils import reset
from django.shortcuts import render
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from apps.authentication.models import Profile
from .serializers import PostSerializer, UpdateFeedCategorySerializer, PostCreateSerializer
from .models import Post, PostFeedIndex
from typing	 import TypeAlias
from rest_framework.response import Response
import base64

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
      category = PostFeedIndex.getRecentCategory()
      query = Post.getRecentPosts(category.index_name).prefetch_related('created_by', 'created_by__user', 'postmedia_set', 'likes')
      serializer = PostSerializer(query, many = True, context={'profile': user})
      return Response({"data" : serializer.data, "feed_category": category.index_name, "updated_at": category.updated_at })


class UpdateFeed(APIView):
  [IsAuthenticated]
  def post(self, request, *args, **kwargs):
    serializer = UpdateFeedCategorySerializer(data = request.data)
    def checkUpdates(objectList, feedCategory, lastUpdate):
      for obj in objectList:
        if obj['feed_category'] == feedCategory:
          if datetime.fromisoformat(obj['last_update']).strftime("%m/%d/%Y %H:%M:%S") == lastUpdate.strftime("%m/%d/%Y %H:%M:%S"):
            return False
          return True
      return True
    if serializer.is_valid():
      print('valido')
      data = serializer.data
      feed = PostFeedIndex.getRecentPostFeed().order_by('-id')
      
      for feedIndex in feed[:10]:
        indexName = feedIndex.index_name
  
        updates = checkUpdates(data['categories'],indexName , feedIndex.updated_at)
        if (updates):
          user = Profile.getByRequest(request)
          query = Post.getRecentPosts(indexName).prefetch_related('created_by', 'created_by__user', 'postmedia_set', 'likes')
          serializer = PostSerializer(query, many = True, context={'profile': user})
          return Response({"data" : serializer.data, "feed_category": indexName, "updated_at": feedIndex.updated_at })
      return Response("Tudo em dia!", status=status.HTTP_204_NO_CONTENT)
    return redirect("get_feed_posts")
  
class PostCreateAPIView(APIView):
  def post(self, request, *args, **kwargs):
      serializer = PostCreateSerializer(data=request.data, context={'request': request})
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)