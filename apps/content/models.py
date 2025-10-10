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
     comments_enabled = models.BooleanField(default=True)


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


     def __str__(self):
          return f"Bu file ushbu niki{self.post.short_id} - {self.file.name}"



class Comment(BaseModel):
     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
     content = models.TextField()


     def __str__(self):
          return f"{self.user.username} {self.post.short_id} postiga comment qoldirdi" 



class Like(BaseModel):
     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')


     def __str__(self):
          return f"{self.user.username} {self.post.short_id} postiga like bosdi"



class PostSave(BaseModel):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')
     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saves')

     class Meta:
          unique_together = ('user', 'post')
          ordering = ['-created_at']

     def __str__(self):
          return f"{self.user.username} {self.post.short_id} postini saqladi"



class PostShare(BaseModel):
     SHARE_CHOICES = [
          ('direct', 'Direct Share'),
          ('tashqi_share', 'External Share'),
          ('stories', 'Story Share'),
          ('yuklab_olish', 'Download'),
          ('linkdan_kopiya', 'Copy Link'),
     ]

     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_shares')
     receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_shares', verbose_name='qabul qiluvchi')
     share_type = models.CharField(max_length=20, choices=SHARE_CHOICES)
     

     def __str__(self):
          if self.share_type == 'direct' and self.receiver:
               return f"{self.sender.username} → {self.receiver.username} | {self.post.short_id}"
          return f"{self.sender.username} {self.share_type} orqali ulashdi | {self.post.short_id}"



class PostView(BaseModel):
     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_views')

     class Meta:
          unique_together = ('post', 'user')


     def __str__(self):
          return f"{self.user.username} {self.post.short_id} postini ko'rdi"



class CommentLike(BaseModel):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment_likes', null=True, blank=True)
     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')

     
     def __str__(self):
          return f'{self.user.username} {self.comment.id} commentiga like bosdi'



class CommentComment(BaseModel):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment_replies', null=True, blank=True)
     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_replies')
     reply = models.CharField(max_length=255)

     
     def __str__(self):
          return f'{self.user.username} {self.post.short_id} ni commentiga comment yozdi'



class CommentCommentLike(BaseModel):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment_reply_likes', null=True, blank=True)
     comment_comment = models.ForeignKey(CommentComment, on_delete=models.CASCADE, related_name='comment_reply_likes')

     
     def __str__(self):
          return f'{self.user.username} {self.comment_comment.id} commentiga like bosdi'