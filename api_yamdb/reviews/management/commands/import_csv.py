import csv

from django.core.management.base import BaseCommand

from reviews.models import (Category,
                            Comment,
                            GenreTitle,
                            Genre,
                            Review,
                            Title,
                            User)


def import_data():
    with open('static/data/comments.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Comment.objects.create(
                review_id_id=row['review_id'],
                text=row['text'],
                author_id=row['author'],
                pub_date=row['pub_date'],
            )
            
    with open('static/data/category.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Category.objects.create(
                name=row['name'],
                slug=row['slug']
            )


class Command(BaseCommand):
    help = 'Импорт csv в модель "Category"'

    def handle(self, *args, **options):
        import_data()
        self.stdout.write(self.style.SUCCESS('Перенос информации завершен'))
