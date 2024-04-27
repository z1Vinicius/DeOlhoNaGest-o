from django.contrib import admin

from .models import (
  Post,
  PostMedia
)
	
@admin.decorators.register(Post)
class PostAdmin(admin.ModelAdmin):
  ...
  
@admin.decorators.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
  ...