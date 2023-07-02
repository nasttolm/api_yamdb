import pandas as pd

from reviews.models import (Category,
                            Comment,
                            GenreTitle,
                            Genre,
                            Review,
                            Title,
                            User)

csv_files = [
    'api_yamdb/static/data/category.csv',
    'api_yamdb/static/data/comments.csv',
    'api_yamdb/static/data/genre_title.csv',
    'api_yamdb/static/data/genre.csv',
    'api_yamdb/static/data/review.csv',
    'api_yamdb/static/data/titles.csv',
    'api_yamdb/static/data/users.csv'
]

mappings = [
    {
        'id': 'id',
        'name': 'name',
        'slug': 'slug'
    },
    {
        'id': 'id',
        'review_id': 'review__id',
        'text': 'text',
        'author': 'author__id',
        'pub_date': 'pub_date'
    },
    {
        'id': 'id',
        'title_id': 'genre_id',
        'genre_id': 'title_id'
    },
    {
        'id': 'id',
        'name': 'name',
        'slug': 'slug'
    },
    {
        'id': 'id',
        'title_id': 'title_id',
        'text': 'text',
        'author': 'author',
        'score': 'score',
        'pub_date': 'pub_date'
    },
    {
        'id': 'id',
        'name': 'name',
        'year': 'year',
        'category': 'category'
    },
    {
        'id': 'id',
        'username': 'username',
        'email': 'email',
        'role': 'role',
        'bio': 'bio',
        'first_name': 'first_name',
        'last_name': 'last_name'
    }
]

for i, csv_file in enumerate(csv_files):
    model = [Category, Comment, GenreTitle, Genre, Review, Title, User]
    mapping = mappings[i]

    df = pd.read_csv(csv_file)
    for _, row in df.iterrows():
        model_instance = model[i]()
        for key, value in mapping.items():
            setattr(model_instance, key, row[value])
        obj, created = model[i].objects.get_or_create(
            **model_instance.__dict__)
        if created:
            obj.save()

    print(f'Импортировано {len(df)} строк из файла {csv_file}.')
