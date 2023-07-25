from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoginView

# 라우터 생성
router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # 다른 URL 패턴들을 필요에 따라 추가할 수 있습니다.
    path('', include(router.urls)),
    path('rest-auth/', include('dj_rest_auth.urls')),
]
