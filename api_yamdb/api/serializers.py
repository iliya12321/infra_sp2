from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api_yamdb.settings import (
    EMAIL_MAX_LENGTH,
    USER_NAME_MAX_LENGTH
)
from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import validate_year, validate_username


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=USER_NAME_MAX_LENGTH,
        required=True,
        validators=[
            validate_username,
            UniqueValidator(queryset=User.objects.all()),
        ]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        lookup_field = 'username'


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USER_NAME_MAX_LENGTH,
        required=True,
        validators=[validate_username]
    )
    confirmation_code = serializers.CharField(required=True)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH
    )
    username = serializers.CharField(
        max_length=EMAIL_MAX_LENGTH,
        validators=[validate_username]
    )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        request = self.context['request']
        author = request.user
        title = get_object_or_404(Title, id=title_id)
        if (
            title.reviews.filter(author=author).exists()
            and request.method != 'PATCH'
        ):
            raise serializers.ValidationError(
                'Можно оставлять только один отзыв!'
            )
        return data


class CategoryGenre(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class CategorySerializer(CategoryGenre):

    class Meta(CategoryGenre.Meta):
        model = Category


class GenreSerializer(CategoryGenre):

    class Meta(CategoryGenre.Meta):
        model = Genre


class TitleCreateAndUpdateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'name', 'year', 'description', 'category', 'genre', 'id', 'rating'
        )
        read_only_fields = fields
