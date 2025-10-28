from rest_framework import serializers
from apps.base.models import BaseModel
from apps.users.models import User
from apps.content.models import Post, PostFiles, Comment, Tag, Like, PostSave, PostShare, PostView, CommentLike, CommentComment, CommentCommentLike
from apps.users.serializers import UserProfileDataSerializers




class PostFilesSerializers(serializers.ModelSerializer):
     file_url = serializers.SerializerMethodField()

     class Meta:
          model = PostFiles
          fields = ['id', 'file', 'file_url', 'count', 'order']

     def get_file_url(self, obj):
          request = self.context.get('request')
          if obj.file and request:
               return request.build_absolute_uri(obj.file.url)
          return None



class PostSerializer(serializers.ModelSerializer):
     user = UserProfileDataSerializers(read_only=True)
     files = PostFilesSerializers(many=True, read_only=True)
     tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
     short_id = serializers.SerializerMethodField()

     class Meta:
          model = Post
          fields = ['id', 'short_id', 'user', 'files', 'caption', 'location', 'tags', 'comments_enabled', ]

     def get_short_id(self, obj):
          return obj.short_id
     
     def create(self, validated_data):
          tags_data = validated_data.pop('tags', [])
          post = Post.objects.create(user=self.context['request'].user, **validated_data)
          post.tags.set(tags_data)
          return post    