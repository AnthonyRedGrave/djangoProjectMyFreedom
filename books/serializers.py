from rest_framework.serializers import ModelSerializer
from .models import Book, Genre, Publisher
from rest_framework import serializers


# API - Application Programming Interface Список команд, благодаря которым можно работать с сервером


class CreateBookSerializer(ModelSerializer):

    tags_ids = serializers.CharField()

    def validate_tags_ids(self, value: str):
        # из строки сделать список

        # продолжить валидировать переданные теги
        value = value.split(', ')

        print(value)

        return "Теги"

    class Meta:
        model = Book
        fields = ['title', 'author', 'year', 'price', 'raiting', 'genre', 'tags_ids']


class GenreBookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'count']


class GenreSerializer(ModelSerializer):
    books = GenreBookSerializer(many=True)

    class Meta:
        model = Genre
        fields = ["id", "title", "books"]


class PublisherSerializer(ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'title', 'language']


class BookSerializer(ModelSerializer):
    genre_title = serializers.SerializerMethodField()
    publisher_title = serializers.SerializerMethodField()

    tags_titles = serializers.SerializerMethodField()


    def get_tags_titles(self, book):
        tags = []
        for tag in book.tags.all():
            tags.append(tag.title)

        return tags

    def get_publisher_title(self, book):
        if book.publisher is not None:
            return book.publisher.title
        return "Нет издателя"

    def get_genre_title(self, book):
        try:
            return book.genre.title
        except AttributeError:
            return "Нет жанра"

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "genre_title",
            "publisher_title",
            "count",
            "price",
            "tags_titles",
        ]
