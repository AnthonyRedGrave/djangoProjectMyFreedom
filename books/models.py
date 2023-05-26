from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    year = models.IntegerField()
    raiting = models.IntegerField(default=0)

    publisher = models.CharField(max_length=50, null=True)

    genre = models.ForeignKey("Genre", on_delete=models.DO_NOTHING, null=True, blank=True, related_name='books')

    def __str__(self):
        # строковое представление объекта
        return f"Книга: {self.id} Название: {self.title} Автор: {self.author}"


class Genre(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return f"Жанр: {self.id}, {self.title}"

