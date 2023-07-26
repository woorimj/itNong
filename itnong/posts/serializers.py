from .models import Post, Liked
from rest_framework import serializers
from django.contrib.auth import get_user_model

class PostSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source = 'writer.username')

    class Meta:
        model = Post
        fields = ['id','title', 'content', 'photo', 'created_at', 'area', 'city', 'prices', 'links', 'writer' ]

class LikedSerializer(serializers.ModelSerializer):
     class Meta:
        model = Liked
        fields = '__all__'