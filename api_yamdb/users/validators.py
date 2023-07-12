from django.core.validators import RegexValidator


username_regular = RegexValidator(
    r'^[\w.@+-]+\Z',
    'Поддерживаются только буквы, цифры и знаки @.+-_')
