from datetime import datetime
from typing import TypeAlias

from axes.utils import reset
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView, status

from apps.authentication.models import Profile
from .models import Post, PostFeedIndex
from .serializers import PostSerializer, UpdateFeedCategorySerializer, PostCreateSerializer, PostStatusUpdateSerializer

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
    
class LikeUnlikePostAPIView(APIView):
  def post(self, request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = Profile.getByRequest(request)
    
    if post.likes.filter(pk=user.pk).exists():
      return Response({"detail": "Você já curtiu este post."}, status=status.HTTP_400_BAD_REQUEST)
    
    post.likes.add(user)
    post.like_count += 1
    post.save()
      
    return Response({"detail": "Você curtiu este post."}, status=status.HTTP_200_OK)

  def delete(self, request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = Profile.getByRequest(request)
    
    if not post.likes.filter(pk=user.pk).exists():
        return Response({"detail": "Você ainda não curtiu este post."}, status=status.HTTP_400_BAD_REQUEST)
    
    post.likes.remove(user)
    post.like_count -= 1
    post.save()
    
    return Response({"detail": "Você removeu o like deste post."}, status=status.HTTP_200_OK)
  
class UpdatePostStatusAPIView(APIView):
  def put(self, request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = Profile.getByRequest(request)
    if post.created_by.id == user.id:
      serializer = PostStatusUpdateSerializer(instance=post)
      serializer.update(post, {})
      return Response({'detail': 'Status do post atualizado para "private".'}, status=status.HTTP_200_OK)
    else:
      return Response({'detail': 'O campo created_at na requisição não corresponde ao created_at do post.'}, status=status.HTTP_400_BAD_REQUEST)