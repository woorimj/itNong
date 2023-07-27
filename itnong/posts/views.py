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
class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            # 아마 여기는.. 프론트에서 클릭시 되는걸로 해야하지 않을까?
            # 그래서 일단은 임시함수이름을 써놓음
            if like_post(request.user, post_id):
                like_count = Liked.objects.filter(post=post_id).count()
            # 취소시
            like_count = Liked.objects.filter(post=post_id).count()

        except TypeError:
            return Response(
                {"detail": "로그인상태나 게시글을 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Post.DoesNotExist:
            return Response(
                {"detail": "존재하지 않는 게시글입니다"}, status=status.HTTP_404_NOT_FOUND
            )
