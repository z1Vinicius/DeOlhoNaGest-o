from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from uuid import uuid4

from apps.authentication.models import Profile
MEDIA_ROOT_POST = 'post/media'

POST_STATUS = (
    ("public", "Público"),
    ("private", "Privado"),
    ("withheld", "Retido"),
    ("deleted", "Deletado")
    
)

class Post(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid4, db_column="CD_POST")
    created_by = models.ForeignKey(Profile, on_delete= models.CASCADE, verbose_name="Criado por", db_column="CREATED_BY")
    created_at = models.DateTimeField(auto_created= True, verbose_name="Criado em", db_column="CREATED_AT")
    updated_at = models.DateTimeField(blank = True, null= True, verbose_name="Atualizado em", db_column="UPDATED_AT")
    post_text = models.CharField(max_length= 500, blank= False, null= False, verbose_name="Texto", db_column="POST")
    likes = models.ManyToManyField(Profile,  verbose_name="Curtidas", db_column="LIKE", related_name="post_likes")
    like_count = models.IntegerField(null= True, verbose_name="Quantidade de curtidas", db_column="QT_LIKE")
    status = models.CharField(
        max_length= 15,
        choices = POST_STATUS,
        default= 'public'
    )
    
    def __str__(self):
        return self.post_text

class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, verbose_name="Postagem", db_column="CD_POST")
    image = models.ImageField(upload_to= MEDIA_ROOT_POST, blank= True, verbose_name="Imagem",db_column="PATH")
