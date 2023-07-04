import django_filters

from reviews.models import Category, Genre, Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains',
        label='Категория'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains',
        label='Жанр'
    )
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Название произведения'
    )
    year = django_filters.NumberFilter(
        field_name='year',
        lookup_expr='exact',
        label='Год выпуска'
    )

    class Meta:
        Model = Title
        fields = ('category', 'genre', 'name', 'year')
