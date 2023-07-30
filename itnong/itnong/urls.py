from django.contrib import admin
from django.urls import path, include
from posts import urls
from accounts import urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("posts.urls")),
    path("", include("accounts.urls")),
]
