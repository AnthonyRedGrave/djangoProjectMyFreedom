from django.shortcuts import render
from .models import Book, Genre


def books(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    return render(request, "index.html", context={"books": books,
                                                  "genres": genres})

