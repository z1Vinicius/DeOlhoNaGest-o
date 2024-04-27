from rest_framework import serializers
from .models import Post, PostMedia

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
        'likes': instance.like_count,
        'media': PostMediaSerializer(instance.postmedia_set.all(), many = True).data,
        'description': instance.post_text    
      },
      'profile': {
        'created_by': instance.created_by.id,
        'name': instance.created_by.user.first_name,
        'lastName': instance.created_by.user.last_name,
        'profileImage': instance.created_by.avatar.url
      }
    }