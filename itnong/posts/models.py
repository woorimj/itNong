from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    AREA_IN_CHOICES = (
        ('서울특별시', '서울특별시'),
        ('인천광역시', '인천광역시'),
        ('대전광역시', '대전광역시'),
        ('대구광역시', '대구광역시'),
        ('울산광역시', '울산광역시'),
        ('부산광역시', '부산광역시'),
        ('광주광역시', '광주광역시'),
        ('세종특별자치시', '세종특별자치시'),
        ('경기도', '경기도'),
        ('강원특별자치도', '강원특별차지도'),
        ('충청북도', '충청북도'),
        ('충청남도', '충청남도'),
        ('전라북도', '전라북도'),
        ('전라남도', '전라남도'),
        ('경상북도', '경상북도'),
        ('경상남도', '경상남도'),
        ('제주특별자치도', '제주특별자치도')
    )
        
    title = models.CharField(max_length=128)
    content = models.TextField(verbose_name="내용")
    photo = models.ImageField(verbose_name="이미지", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="작성일", auto_now_add=True)
    area = models.CharField(verbose_name="지역", max_length=10, choices=AREA_IN_CHOICES)
    prices = models.CharField(max_length=20)
    links = models.URLField(max_length=1024)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
    
# 관심글모델    
class Liked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE) 

    class Meta:
        # 관심글 중복방지
        unique_together = ('user', 'post')

        