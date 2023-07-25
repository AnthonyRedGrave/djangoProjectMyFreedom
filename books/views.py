from django.shortcuts import render, redirect
from .models import Book, Genre, Tag, Publisher, Comment, Favorite
from .forms import BookForm
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import JsonResponse

from .serializers import BookSerializer, GenreSerializer, CreateBookSerializer, PublisherSerializer
from rest_framework.decorators import api_view


def get_all_publishers(request):
    publishers = Publisher.objects.all()
    serializer = PublisherSerializer(publishers, many=True)
    return JsonResponse(data=serializer.data, safe=False)


def get_all_genres(request):
    genres = Genre.objects.all()

    serializer = GenreSerializer(genres, many=True)
    return JsonResponse(data = serializer.data, safe=False)

def get_all_books(request):
    # вьюшка должна возвращать все книги в json формате
    # сделать запрос в бд и получить все книги
    # все книги необходимо сериализовать
    # вернуть все книги в json формате
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)

    return JsonResponse(data=serializer.data, safe=False)


def book_detail(request, id):
    try:
        book = Book.objects.get(id = id)
    except Book.DoesNotExist:
        return JsonResponse(data={"id":"Book not found!"})

    serializer = BookSerializer(book)

    return JsonResponse(data=serializer.data)

@api_view(['POST',])
def create_book(request):
    # request.POST - тело запроса
    # с request.POST можно работать как с обычным словарем
    # вызываю сериализатор для валидации данных
    serializer = CreateBookSerializer(data=request.POST)

    if serializer.is_valid():
        print("все данные валидны")
    else:
        print(serializer.errors)
        return JsonResponse(data = serializer.errors)

    # serializer.validated_data - словарь в котором находятся "чистые" данные
    # book = Book.objects.create(**serializer.validated_data)
    # book.tags.set()
    #
    # # второй сериализатор использую для формирования ответа
    # serializer = BookSerializer(book)
    # return JsonResponse(data = serializer.data)
    return JsonResponse(data = {"da": "ahsdihas"})


class BookListView(ListView):
    model = Book
    context_object_name = 'my_new_books'
    queryset = Book.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        # получение первоначального контекста
        context = super().get_context_data(**kwargs)

        # запрос в бд получить все теги
        tags = Tag.objects.all()

        # добавление в контекст новую пару
        context['tags'] = tags

        # get_context_data обязательно возвращает контекст
        return context


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        # получение первоначального контекста
        context = super().get_context_data(**kwargs)

        # получение книги
        book = self.get_object()
        show_favorite_button = True

        # если пользователь авторизован, только в таком случае
        # идем смотреть добавлял ли пользователь в избранное книгу
        if self.request.user.is_authenticated:
            if Favorite.objects.filter(book=book, user=self.request.user):
                show_favorite_button = False

        context['show_favorite_button'] = show_favorite_button

        return context


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
    return render(
        request, "tag_detail.html", context={"tag_books": tag_books, "tag": tag}
    )


def add_book(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            form = BookForm()
            return render(request, "add_book.html", context={"form": form})
        elif request.method == "POST":
            publisher_id = request.POST["publisher"]
            genre_id = request.POST["genre"]

            publisher = None
            genre = None
            image = request.FILES.get("image", "default.jpg")

            if publisher_id != "":
                publisher = Publisher.objects.get(id=publisher_id)

            if genre_id != "":
                genre = Genre.objects.get(id=genre_id)

            book = Book.objects.create(
                title=request.POST["title"],
                author=request.POST["author"],
                year=request.POST["year"],
                raiting=request.POST["raiting"],
                publisher=publisher,
                genre=genre,
                image=image,
                user=request.user,
            )
            tags = request.POST.getlist("tags")
            book.tags.set(tags)
            book.save()

            return redirect("books")
    else:
        return HttpResponse("<h1>У вас нет прав на это действие!</h1>")


def search_book_by_tags(request):
    # получаем строку которую ввел юзер из тела ГЕТ запроса
    tags_input:str = request.GET['tags_input']

    # инициализируем пустой список для будущих сообщений об ошибках
    messages = []

    # превращаем строку из тела запроса в список с разделителем ", "
    tags_list = tags_input.split(', ')

    # инициализируем пустой список с найденными тегами
    tags = []

    # список со всеми книгами у этих найденных тегов
    tag_books = []

    # проходимся по списку из тегов, который ввел юзер
    for tag_title in tags_list:
        try:
            # если тега с таким title не существует
            # заполняем список messages для отображения ошибок на странице

            # в обратном случае - добавляем найденный тег (объект) в список tags
            tag = Tag.objects.get(title = tag_title)
            tags.append(tag)
        except Tag.DoesNotExist:
            messages.append(f"Тега с таким названием не существует! {tag_title}")

    # проходимся по списку (list) из найденных тегов
    # у каждого тега есть книги, через related_name books и all()
    # получаем список (queryset) из всех книг у данного тега
    # и запихиваем книгу в список tag_books
    for tag in tags:
        for book in tag.books.all():
            tag_books.append(book)


    # могут попасться дубликаты книг, благодаря функции set мы избавляемся от дублей
    return render(
        request, "tag_detail.html", context={"tag_books": set(tag_books),
                                             "tag": None,
                                             "messages": messages}
    )


def search_book(request):
    title = request.GET["title"]
    genre = request.GET["genre"]
    price_lt = request.GET["price_lt"]

    books = Book.objects.all()

    result_string = "Результат поиска "

    if title != "":
        result_string += f"по названию: {title}, "
        books = books.filter(title__contains=title)

    if genre != "":
        result_string += f"по жанру: {genre}, "
        books = books.filter(genre__title__contains=genre)

    if price_lt != "":
        result_string += f"по цене до: {price_lt}, "
        books = books.filter(price__lte=price_lt)

    return render(
        request,
        "search_book.html",
        context={"books": books, "result_string": result_string},
    )


def delete_book(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponse(f"<h1>Книги с таким айди: {id} не существует!</h1>")

    if request.user.username != book.user.username:
        return HttpResponse("<h1>У вас нет прав на обновление этой книги!</h1>")
    else:
        book.delete()
        return redirect("books")


def update_book(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponse(f"<h1>Книги с таким айди: {id} не существует!</h1>")

    if request.user.username != book.user.username:
        return HttpResponse("<h1>У вас нет прав на обновление этой книги!</h1>")

    else:
        if request.method == "GET":
            form = BookForm(instance=book)

            return render(
                request, "update_book.html", context={"form": form, "book": book}
            )
        else:
            publisher_id = request.POST["publisher"]
            genre_id = request.POST["genre"]

            publisher = None
            genre = None
            image = request.FILES.get("image", "default.jpg")

            if publisher_id != "":
                publisher = Publisher.objects.get(id=publisher_id)

            if genre_id != "":
                genre = Genre.objects.get(id=genre_id)

            book.title = request.POST["title"]
            book.author = request.POST["author"]
            book.year = request.POST["year"]
            book.raiting = request.POST["raiting"]
            book.publisher = publisher
            book.genre = genre
            book.image = image
            tags = request.POST.getlist("tags")
            book.tags.set(tags)

            book.save()

            return redirect("get_book", pk=book.id)


def add_comment(request, id):
    if request.user.is_authenticated:
        raiting = 5

        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return HttpResponse("<h1>Такой книги не существует</h1>")

        try:
            Comment.objects.create(
                content=request.POST["comment"],
                raiting=raiting,
                user=request.user,
                book=book,
            )
        except MultiValueDictKeyError:
            return HttpResponse("<h1>404</h1>")
        return redirect("get_book", pk=id)
    else:
        return HttpResponse("<h1>Вы не авторизованы в системе!</h1>")


def buy_book(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponse("<h1>Такой книги не существует!</h1>")

    if book.count != 0:
        book.count = book.count - 1
        book.save()
    else:
        return HttpResponse("<h1>404</h1>")

    return HttpResponse("<h1>Страница покупки</h1>")


def favorite_book(request, id):
    try:
        book = Book.objects.get(id = id)
    except Book.DoesNotExist:
        return HttpResponse('<h1>404</h1>')

    if not request.user.is_authenticated:
        return HttpResponse('<h1>404</h1>')

    Favorite.objects.create(book = book,
                            user = request.user)

    return redirect("get_book", pk=book.id)


def favorites(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        return render(
            request, "favorites.html", context={"favorites": favorites}
        )
    else:
        return HttpResponse('<h1>404</h1>')


def delete_from_favorites(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponse('<h1>404</h1>')

    if request.user.is_authenticated:

        favorite = Favorite.objects.get(user = request.user, book = book)

        favorite.delete()

        return redirect('favorites')

    return HttpResponse('<h1>404</h1>')


