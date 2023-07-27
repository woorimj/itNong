from .models import Post, Liked
from .serializers import PostSerializer, LikedSerializer

from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny


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
