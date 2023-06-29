from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg

from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from reviews.models import (User,
                            Category,
                            Genre,
                            Title,
                            Review)
from .serializers import (UserGetTokenSerializer,
                          UserRegistrationSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          ReviewSerializer)
from .permissions import AdminOrReadOnly


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Код подтверждения регистрации',
                f'{confirmation_code}',
                'yamdb.host@yandex.ru',
                [serializer.validated_data.get('email')],
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGetTokenView(APIView):
    def post(self, request):
        serializer = UserGetTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            user = get_object_or_404(User, username=username)
            token = serializer.validated_data.get('confirmation_code')
            confirmation_code = default_token_generator.check_token(
                user, token)
            if not confirmation_code:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            refresh = RefreshToken.for_user(user)
            return Response(
                {'token': str(refresh.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly, )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly, )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating = Title.reviews.aggregate(Avg("score")))
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly, )
