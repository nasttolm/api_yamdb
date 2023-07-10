from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, StringRelatedField

from reviews.models import (User,
                            Category,
                            Genre,
                            Title,
                            Review,
                            Comment)


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {'Выберите другой username'})
        return data


class UserGetTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255, read_only=True)
    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField(max_length=256)


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.SlugField(max_length=50)

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.SlugField(max_length=50)

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    genre = SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleGETSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        model = Title
        read_only_fields = ('genre', 'category', 'rating')


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('author', 'pub_date', 'title')

    def validate(self, data):
        if Review.objects.filter(
            author=self.context['request'].user,
            title_id=self.context['view'].kwargs.get('title_id')
        ).exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Нельзя оставить два отзыва на одно произведение.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = StringRelatedField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,
                                     max_length=150)
    email = serializers.EmailField(required=True,
                                   max_length=254)

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        model = User
