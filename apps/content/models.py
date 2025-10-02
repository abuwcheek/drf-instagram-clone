from django.db import models
from base.models import BaseModel
from users.models import User



class Tag(BaseModel):
     name = models.CharField(max_length=50, unique=True)

     def __str__(self):
          return self.name


class Post(BaseModel):
     short_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
     caption = models.TextField(blank=True, null=True)
     image_video = models.FileField(upload_to='posts/')
     location = models.CharField(max_length=255, blank=True, null=True)
     tags = models.ManyToManyField(Tag, blank=True, related_name='tags')
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     