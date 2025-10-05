from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to='user_profiles/', 
        blank=True, 
        null=True
    )
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.username