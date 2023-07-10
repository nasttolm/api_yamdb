from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import year_validator, slug_validator, username_regular


CHAR_REQUIRED_NUMBER = 16
ROLES = [
    ('U', 'user'),
    ('M', 'moderator'),
    ('A', 'admin')
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_regular],
        verbose_name='Юзернейм пользователя'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Отчество пользователя'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография пользователя'
    )
    role = models.CharField(
        max_length=2,
        choices=ROLES,
        default=ROLES[0][0],
        verbose_name='Роль пользователя'
    )

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f'Пользователь {self.first_name} {self.last_name}'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[slug_validator],
        verbose_name='Идентификатор категории'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:CHAR_REQUIRED_NUMBER]


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[slug_validator],
        verbose_name='Идентификатор жанра'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:CHAR_REQUIRED_NUMBER]


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(
        validators=[year_validator],
        verbose_name='Год выпуска',
        null=True,
        blank=True
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        through='GenreTitle',
        verbose_name='Жанр',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:CHAR_REQUIRED_NUMBER]


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    def __str__(self):
        return f'У произведения "{self.title}", жанр: {self.genre}'


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка произведения'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации отзыва'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title_id'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:CHAR_REQUIRED_NUMBER]


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария',
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:CHAR_REQUIRED_NUMBER]
