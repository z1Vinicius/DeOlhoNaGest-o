from django.contrib import admin

from .models import (
   Profile
)
	
@admin.decorators.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
   ...