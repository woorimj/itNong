from rest_framework.serializers import ModelSerializer
from .models import Post, Liked, Comment, Reply
from rest_framework import serializers
from django.contrib.auth import get_user_model


class PostSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="writer.username")
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return Liked.objects.filter(post=obj.id).count()
    
    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj.id)
        return CommentSerializer(comments, many=True).data
    
    def get_replies(self, obj):
        replies = Reply.objects.filter(comment__post=obj.id)
        return ReplySerializer(replies, many=True).data

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "photo",
            "created_at",
            "area",
            "city",
            "prices",
            "links",
            "writer",
            "likes",
            "comments",
            "replies",
        ]


class LikedSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = Liked
        fields = ["id", "post", "user"]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [ 'comment', 'post', 'is_secret']

class ReplySerializer(ModelSerializer):
    class Meta:
        model = Reply
        fields = ['reply', 'is_secret']