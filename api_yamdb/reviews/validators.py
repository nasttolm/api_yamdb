from django.utils import timezone

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(
            'Введите корректный год'
        )


slug_validator = RegexValidator(
    r'^[-a-zA-Z0-9_]+$',
    'Поддерживаются только латинские буквы, - и _'
)

username_regular = RegexValidator(
    r'^[\w.@+-]+$',
    'Поддерживаются только буквы, цифры и знаки @.+-_')
