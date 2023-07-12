from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from reviews.models import User


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
