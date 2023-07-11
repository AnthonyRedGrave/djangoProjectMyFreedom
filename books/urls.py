from django.urls import path
from books.views import (
    books,
    get_book,
    get_genre_books,
    get_tag_books,
    add_book,
    search_book,
    delete_book,
    update_book,
    add_comment,
    buy_book,
    favorite_book,
    favorites,
    delete_from_favorites
)


urlpatterns = [
    path("get_books/", books, name="books"),
    path("get_books/<int:id>/", get_book, name="get_book"),
    path("get_genre/<str:title>/", get_genre_books, name="get_genre"),
    path("get_tag/<str:title>/", get_tag_books, name="get_tag_books"),
    path("add_book/", add_book, name="add_book"),
    path("update_book/<int:id>/", update_book, name="update_book_by_id"),
    path("seach_book/", search_book, name="search_book"),
    path("delete_book/<int:id>/", delete_book, name="delete_book"),
    path("add_comment/<int:id>/", add_comment, name="add_comment"),
    path("buy_book/<int:id>/", buy_book, name="buy_book"),
    path("favorite/<int:id>/", favorite_book, name="favorite_book"),
    path("favorites/", favorites, name="favorites"),
    path("delete_from_favorites/<int:id>/", delete_from_favorites, name="delete_from_favorites")
]
