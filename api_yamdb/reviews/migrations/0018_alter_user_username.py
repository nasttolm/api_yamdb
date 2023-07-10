# Generated by Django 3.2 on 2023-07-10 11:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0017_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Поддерживаются только буквы, цифры и знаки @.+-_', regex='^[\\w.@+-]+$')], verbose_name='Юзернейм пользователя'),
        ),
    ]
