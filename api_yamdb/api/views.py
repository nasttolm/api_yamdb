from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from django.core.mail import send_mail
from rest_framework import status, viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import (User,
                            Category,
                            Genre,
                            Title,
                            Review,
                            Comment)
from .serializers import (CommentSerializer,
                          ReviewSerializer,
                          TitleGETSerializer,
                          UserGetTokenSerializer,
                          UserRegistrationSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          TitleGETSerializer,
                          ReviewSerializer,
                          CommentSerializer,
                          UserSerializer
                          )

from .permissions import (AdminOrReadOnly,
                          AuthorAdminModerOrReadOnly,
                          AdminPermission)
from .filters import TitleFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.validated_data['role'] = request.user.role
                serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


def create_code(username):
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        "Подтверждение регистрации на YaMDb!",
        "Для подтверждения регистрации отправьте код:"
        f"{confirmation_code}",
        "yamdb.host@yandex.ru",
        [user.email],
        fail_silently=False,
    )


class UserRegistrationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        serializer = UserRegistrationSerializer(data=request.data)
        if User.objects.filter(username=username, email=email).exists():
            create_code(
                username
            )
            return Response(
                {'email': serializer.initial_data['email'],
                 'username': serializer.initial_data['username']},
                status=status.HTTP_200_OK)
        if serializer.is_valid():
            user = serializer.save()
            confirmation_code = default_token_generator.make_token(user)
            # send_mail(
            #     'Код подтверждения регистрации',
            #     f'{confirmation_code}',
            #     'yamdb.host@yandex.ru',
            #     [serializer.validated_data.get('email')],
            # )
            print(confirmation_code)
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
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response('При заполнении полей ошибка.',
                        status=status.HTTP_400_BAD_REQUEST)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response('При заполнении полей ошибка.',
                        status=status.HTTP_400_BAD_REQUEST)


class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response('При заполнении полей ошибка.',
                        status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModerOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModerOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_title().comments

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = Pagination

    @action(methods=['GET', 'PATCH'], detail=True, url_path='me')
    def get_patch_current_user(self, request):
        if request.method == 'GET':
            data = User.objects.all().filter(username=request.user).values(
                'username', 'email', 'first_name', 'last_name', 'bio', 'role')
            return Response(data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                return self.update(request)
            return Response('При заполнении полей ошибка.',
                            status=status.HTTP_400_BAD_REQUEST)
