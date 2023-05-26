from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    year = models.IntegerField()

    def __str__(self):
        # строковое представление объекта
        return f"Книга: {self.id} Название: {self.title} Автор: {self.author}"
