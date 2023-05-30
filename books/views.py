from django.shortcuts import render
from .models import Book


def books(request):
    books = Book.objects.all()
    return render(request, "index.html", context={"books": books,
                                                  "name": "Олег"})

