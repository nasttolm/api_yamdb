# Generated by Django 3.2 on 2023-07-10 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0013_rename_title_id_review_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='review_id',
            new_name='review',
        ),
    ]
