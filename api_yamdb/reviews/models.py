from django.contrib.auth.models import AbstractUser
from django.db import models


CHAR_REQUIRED_NUMBER = 16
ROLES = [
    'user',
    'moderator',
    'admin'
]
SCORES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


class User(AbstractUser):
    username = models.SlugField(max_length=150, unique=True)
    email = models.SlugField(max_length=254)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(choices=ROLES, default=ROLES[0])


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.CharField(choices=SCORES, default=ROLES[0])
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(
        'Дата публикации отзыва', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title_id'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:CHAR_REQUIRED_NUMBER]


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments')
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата публикации отзыва', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:CHAR_REQUIRED_NUMBER]
