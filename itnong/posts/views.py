from django.shortcuts import get_object_or_404
from .models import Post, Liked, Comment, Reply
from .serializers import PostSerializer, LikedSerializer, CommentSerializer, ReplySerializer

from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet


# Blog의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated | AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(writer=self.request.user)
        else:
            # 로그인하지 않은 사용자의 경우, writer 필드를 None 또는 기본값으로 설정
            serializer.save(writer=None)  # 또는 기본값으로 설정할 값 사용


# 관심 게시글 추가
class LikeView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikedSerializer

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Liked.objects.filter(post=post_id, user=self.request.user)

    def perform_create(self, serializer):
        post_id = self.kwargs["post_id"]
        post = Post.objects.get(pk=post_id)
        serializer.save(post=post, user=self.request.user)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self, **kwargs): # Override
        id = self.kwargs['post_id']
        # 사용자가 인증되지 않은 경우 비밀 댓글은 보이지 않도록 필터링
        if not self.request.user.is_authenticated:
            return self.queryset.filter(post=id, is_secret=False)
        return self.queryset.filter(post=id)
    

class ReplyViewSet(ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def get_queryset(self, **kwargs):
        comment_id = self.kwargs['comment_id']
        if not self.request.user.is_authenticated:
            return self.queryset.filter(comment=comment_id, is_secret=False)
        return self.queryset.filter(comment=comment_id)
    
    def perform_create(self, serializer):
        comment_id = self.kwargs["comment_id"]
        comment = get_object_or_404(Comment, id=comment_id)
        serializer.save(comment=comment)
