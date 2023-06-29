from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet)

router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router.urls)),
]
