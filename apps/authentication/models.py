from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models

MEDIA_ROOT_USER = 'authentication/profile_images'

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  avatar = models.ImageField(upload_to = MEDIA_ROOT_USER, default=r"profile_images\user_placeholder.png")
  phone_number = models.CharField(blank = True, default='', max_length= 20)

  def __str__(self):
      return self.user.username
    
  @classmethod
  def getUserProfile(cls, username):
      userPlaceholder = r'\media\profile_images\user_placeholder.png'
      avatarUrl = cls.objects.filter(user__username = username).first()
      if avatarUrl is None: return userPlaceholder
      return avatarUrl.avatar.url
  
@receiver(post_save, sender= User)
def createProfile(sender, instance, created, **kwargs):
    if(created):
        userProfile = Profile(user = instance)
        userProfile.save()