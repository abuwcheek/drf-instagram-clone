from django.db import models


class BaseModel(models.Model):
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     is_active = models.BooleanField(default=True)  
     is_deleted = models.BooleanField(default=False)
     is_archived = models.BooleanField(default=False)
     is_featured = models.BooleanField(default=False)
     is_verified = models.BooleanField(default=False)
     is_published = models.BooleanField(default=False)


     class Meta:
          abstract = True