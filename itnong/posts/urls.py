from django.urls import path, include
from .views import PostViewSet, LikedCreateAPIView, LikedListAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# 첫 번째 인자는 url의 prefix
# 두 번째 인자는 ViewSet
router.register('posts', PostViewSet)

urlpatterns =[
    path('', include(router.urls)),
    path('liked/', LikedCreateAPIView.as_view(), name='liked-create'),
    #path('<int:pk>/liked/', LikedCreateAPIView.as_view(), name='liked-create'),
    path('liked-lists/', LikedListAPIView.as_view(), name='liked-list'),
]