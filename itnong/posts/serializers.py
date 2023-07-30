from rest_framework.serializers import ModelSerializer
from .models import Post, Comment, Reply, BookMark
from rest_framework import serializers
from django.contrib.auth import get_user_model


class PostSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="writer.username")
    comments = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj.id)
        return CommentSerializer(comments, many=True).data

    def get_replies(self, obj):
        replies = Reply.objects.filter(comment__post=obj.id)
        return ReplySerializer(replies, many=True).data

    def get_bookmarks_count(self, obj):
        return obj.bookmark_set.count()

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
            "comments",
            "replies",
            "bookmarks_count",
        ]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment", "post", "is_secret"]


class ReplySerializer(ModelSerializer):
    class Meta:
        model = Reply
        fields = ["reply", "is_secret"]


class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        fields = "__all__"
