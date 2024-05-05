from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from uuid import uuid4
from datetime import datetime
from django.core.files import File
from django.utils.timezone import now
from os import path
from random import randint
from apps.authentication.models import Profile
MEDIA_ROOT_POST = 'post/media'

POST_STATUS = (
    ("public", "Público"),
    ("private", "Privado"),
    ("withheld", "Retido"),
    ("deleted", "Deletado")
    
)

class PostFeedIndex(models.Model):
    id = models.AutoField(primary_key= True)
    index_name = models.CharField(max_length= 20, unique= True)
    index_count = models.IntegerField(default= 0)
    created_at = models.DateTimeField(auto_now_add= True, verbose_name="Criado em", db_column="CREATED_AT")
    updated_at = models.DateTimeField(auto_now_add= True, verbose_name="Atualizado em", db_column="UPDATED_AT", blank= True, null= True)

    @classmethod
    def createIndex(cls):
        indexName = 'index_' + datetime.now().strftime('%d%m%y%H%M%S%f')
        cls.objects.create(index_name = indexName)
        return indexName
    
    @classmethod
    def getRecentCategory(cls):
        return cls.objects.all().order_by('-id').first().index_name
    
    @classmethod
    def getRecentPostFeed(cls):
        return cls.objects.all()
    
    @classmethod
    def checkMaxIndex(cls, maxIndexCount = 20):
        lastIndex = cls.objects.all().order_by('-id').first()
        if not(lastIndex):
            lastIndex = cls.createIndex()
            lastIndex = cls.objects.all().order_by('-id').first()
        postsIndex = Post.objects.filter(feed_category = lastIndex.index_name)
        if not (lastIndex) or (len(postsIndex) >= maxIndexCount):
            return cls.createIndex()
        return lastIndex.index_name

class Post(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid4, db_column="CD_POST")
    created_by = models.ForeignKey(Profile, on_delete= models.CASCADE, verbose_name="Criado por", db_column="CREATED_BY")
    created_at = models.DateTimeField(auto_now_add= True, verbose_name="Criado em", db_column="CREATED_AT")
    updated_at = models.DateTimeField(blank = True, null= True, verbose_name="Atualizado em", db_column="UPDATED_AT")
    post_text = models.CharField(max_length= 500, blank= False, null= False, verbose_name="Texto", db_column="POST")
    likes = models.ManyToManyField(Profile,  verbose_name="Curtidas", db_column="LIKE", related_name="post_likes")
    like_count = models.IntegerField(default=0, null= True, blank= True, verbose_name="Quantidade de curtidas", db_column="QT_LIKE")
    feed_category = models.CharField(max_length=50, blank= True, null= True)
    status = models.CharField(
        max_length= 15,
        choices = POST_STATUS,
        default= 'public'
    )
    
    def save(self, *args, **kwargs):
        self.feed_category = PostFeedIndex.checkMaxIndex()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.feed_category
    
    @classmethod
    def getAllPosts(cls, createdBy):
        return cls.objects.filter(created_by = createdBy, status = 'public')
    
    @classmethod
    def getRecentPosts(cls, category = ""):
        if not(category):
            category = PostFeedIndex.getRecentCategory()
        return cls.objects.filter(feed_category = category, status = 'public')

class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, verbose_name="Postagem", db_column="CD_POST")
    image = models.ImageField(upload_to= MEDIA_ROOT_POST, verbose_name="Imagem",db_column="PATH")
    
    @classmethod
    def createPostMedia(cls, Post, Path):
        Path = Path.replace("/", "\\")
        filePath = path.normpath(str(path.dirname(path.abspath(__name__))) + Path)
        cls.objects.create(image=filePath, post = Post)