from django.contrib import admin
from .models import Book, Genre, Tag, Publisher


class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "raiting", "year", "publisher", "genre", "get_tags", "created_at", "image", "user")

    def get_tags(self, obj):
        tags = obj.tags.all()
        return "\n".join([t.title for t in tags])


admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Publisher)

