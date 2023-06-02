from django.shortcuts import render
from .models import Book, Genre
from django.http import HttpResponse


#CRUD = CREATE READ! UPDATE DELETE


def books(request):
    books = Book.objects.all()
    return render(request, "index.html", context={"books": books})


def get_book(request, id):

    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponse(f"<h1>Книги с таким айди: {id} не существует!</h1>")

    return render(request, "detail.html", context={"book": book})


def get_genre_books(request, title):
    try:
        genre = Genre.objects.get(title=title)
    except Genre.DoesNotExist:
        return HttpResponse(f"<h1>Жанра с таким названием: {title} не существует!</h1>")

    return render(request, "genre.html", context={"genre": genre})