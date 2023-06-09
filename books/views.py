from django.shortcuts import render
from .models import Book, Genre, Tag, Publisher
from .forms import BookForm
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


def get_tag_books(request, title):
    try:
        tag = Tag.objects.get(title=title)
    except Tag.DoesNotExist:
        return HttpResponse(f"<h1>Тега с таким названием: {title} не существует!</h1>")


    tag_books = tag.books.all()
    return render(request, "tag_detail.html", context={"tag_books": tag_books,
                                                       "tag": tag})


def add_book(request):
    if request.method == "GET":
        form = BookForm()
        return render(request, "add_book.html", context={"form": form})
    elif request.method == "POST":

        publisher_id = request.POST['publisher']
        genre_id = request.POST['genre']

        publisher = Publisher.objects.get(id=publisher_id)
        genre=Genre.objects.get(id=genre_id)
        book = Book(title = request.POST['title'],
                            author = request.POST['author'],
                            year=request.POST['year'],
                            raiting=request.POST['raiting'],
                            publisher=publisher,
                            genre=genre)
        tags = request.POST.getlist('tags')
        book.tags.set(tags)
        book.save()

        form = BookForm()
        return render(request, "add_book.html", context={"form": form})
        # request.POST


# def create_book(request):
#     print(request.POST)
#     genre = Genre.objects.get(id=request.POST['genre'])
#     print(genre)
#     Book.objects.create(title=request.POST['title'],
#                         author=request.POST['author'],
#                         year=request.POST['year'],
#                         tags=request.POST['tags'],
#                         raiting=request.POST['raiting'],
#                         # publisher=request.POST['publisher'],
#                         genre=genre
#                         )
#     return HttpResponse("<h1>Получилось!</h1>")