from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import PostViewSet, LikeView, CommentViewSet, ReplyViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# 첫 번째 인자는 url의 prefix
# 두 번째 인자는 ViewSet
router.register("posts", PostViewSet)

comment_router = SimpleRouter(trailing_slash=True)
comment_router.register("comments", CommentViewSet, basename="comment")

reply_router = SimpleRouter(trailing_slash=True)
reply_router.register("replies", ReplyViewSet, basename="reply")

urlpatterns = [
    path("", include(router.urls)),
    path("posts/<int:post_id>/", include(comment_router.urls)),
    path("posts/<int:post_id>/comments/<int:comment_id>/", include(reply_router.urls)),
    path("liked/", LikeView.as_view(), name="like"),
]
