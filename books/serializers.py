from rest_framework.serializers import ModelSerializer
from .models import Book, Genre
from rest_framework import serializers


class GenreBookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'count']


class GenreSerializer(ModelSerializer):
    books = GenreBookSerializer(many=True)

    class Meta:
        model = Genre
        fields = ["id", "title", "books"]


class BookSerializer(ModelSerializer):
    genre_title = serializers.SerializerMethodField()
    publisher_title = serializers.SerializerMethodField()

    tags_titles = serializers.SerializerMethodField()

    genre = GenreSerializer()

    def get_tags_titles(self, book):
        tags = []
        for tag in book.tags.all():
            tags.append(tag.title)

        return tags

    def get_publisher_title(self, book):
        return book.publisher.title

    def get_genre_title(self, book):
        return book.genre.title

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
            "genre"
        ]
