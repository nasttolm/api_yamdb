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

    with open('static/data/genre_title.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            GenreTitle.objects.create(
                title_id=row['title_id'],
                genre_id=row['genre_id']
            )

    with open('static/data/genre.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Genre.objects.create(
                name=row['name'],
                slug=row['slug']
            )

    with open('static/data/review.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Review.objects.create(
                title_id_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date']
            )

    with open('static/data/titles.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Title.objects.create(
                name=row['name'],
                year=row['year'],
                category_id=row['category']
            )

    with open('static/data/users.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            User.objects.create(
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name']
            )


class Command(BaseCommand):
    help = 'Импорт csv в модель "Category"'

    def handle(self, *args, **options):
        import_data()
        self.stdout.write(self.style.SUCCESS('Перенос информации завершен'))
