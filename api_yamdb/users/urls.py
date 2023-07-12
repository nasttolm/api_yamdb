from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserViewSet, UserRegistrationView, UserGetTokenView

router = DefaultRouter()


router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'auth/signup/',
        UserRegistrationView.as_view(),
        name='user_registration'
    ),
    path(
        'auth/token/',
        UserGetTokenView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path('', include(router.urls)),
]
