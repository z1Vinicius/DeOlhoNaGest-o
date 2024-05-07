from rest_framework import serializers
from .models import Post, PostMedia
from typing import List
from apps.authentication.models import Profile
from django.core.files.base import ContentFile
import base64

class PostMediaSerializer(serializers.ModelSerializer):
  class Meta:
    model = PostMedia
    fields = ['image']
    
  def to_representation(self, instance):
    return instance.image.url

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = ['id', 'created_by', 'created_at', 'post_text', 'like_count']
    
  def to_representation(self, instance):
    return {
      'data': {
        'id': instance.id,
        'createdAt': instance.created_at,
        'updatedAt': instance.updated_at,
        'likes': len(instance.likes.all()),
        'feed_category': instance.feed_category,
        'media': PostMediaSerializer(instance.postmedia_set.all(), many = True).data,
        'hasLike':  self.context.get("profile") in instance.likes.all(),
        'description': instance.post_text    
      },
      'profile': {
        'createdBy': instance.created_by.id,
        'name': instance.created_by.user.first_name,
        'lastName': instance.created_by.user.last_name,
        'profileImage': instance.created_by.avatar.url
      }
    }
    
class FeedCategorySerializer(serializers.Serializer):
  feed_category = serializers.CharField(max_length = 50)
  last_update = serializers.DateTimeField()
    
class UpdateFeedCategorySerializer(serializers.Serializer):
  categories = FeedCategorySerializer(many = True)
  

class PostCreateSerializer(serializers.ModelSerializer):
  media = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

  class Meta:
    model = Post
    fields = ['post_text', 'media']

  def create(self, validated_data):
    mediaData = validated_data.pop('media', [])
    createdBy = Profile.getByRequest(self.context['request'])
    post = Post.objects.create(created_by=createdBy, **validated_data)
    
    for image_data in mediaData:
      imageBinary = base64.b64decode(image_data)
      PostMedia.objects.create(image=ContentFile(imageBinary, name='image.jpg'), post=post)

    return post
  
class PostStatusUpdateSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
      instance.status = 'private'
      instance.save()
      return instance