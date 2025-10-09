from django.db import models
from django.core.validators import FileExtensionValidator
from apps.base.models import BaseModel
from apps.users.models import User
from .shortid import generate_shortcode





class Tag(BaseModel):
     name = models.CharField(max_length=50, unique=True)

     def __str__(self):
          return self.name



class Post(BaseModel):
     short_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
     caption = models.TextField(blank=True, null=True)
     location = models.CharField(max_length=255, blank=True, null=True)
     tags = models.ManyToManyField(Tag, null=True, blank=True, related_name='tags')
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)


     def __str__(self):
          return f"Post by {self.user.username} - {self.short_id}"
     

     def save(self, *args, **kwargs):
          super().save(*args, **kwargs)  # avval saqlab id hosil qilamiz
          if not self.short_id:
               self.short_id = generate_shortcode(self.id)
               super().save(update_fields=["shortcode"])



class PostFiles(BaseModel):
     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='files')
     file = models.FileField(upload_to='post/media/', validators=[FileExtensionValidator(allowed_extensions=('jpg', 'jpeg', 'png', 'heic', 'hd', 'img', 'mp4', 'mov'))])
     count = models.PositiveIntegerField(default=0)
     order = models.PositiveIntegerField(default=0)

     class Meta:
          ordering = ['order']