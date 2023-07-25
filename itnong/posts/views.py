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
class LikedCreateAPIView(generics.CreateAPIView):
    queryset = Liked.objects.all()
    serializer_class = LikedSerializer
    # 로그인 한 사용자만 접근가능
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']  # URL에서 추출한 게시글의 ID
        post = Post.objects.get(pk=post_id)  # 해당 ID에 해당하는 게시글을 가져옴
        serializer.save(user=self.request.user, post=post)  # 좋아요 정보 저장

# 관심 게시글 조회기능
class LikedListAPIView(APIView):
    # 로그인 시
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_posts = Post.objects.filter(liked__user=user)
        #user_liked = Liked.objects.filter(user=request.user)
        serializer = LikedSerializer(liked_posts, many=True)
        return Response(serializer.data)
    
    
