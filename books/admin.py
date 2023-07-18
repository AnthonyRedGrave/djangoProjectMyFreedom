from django.contrib import admin
from .models import Book, Genre, Tag, Publisher, Comment, Favorite


class BookAdmin(admin.ModelAdmin):

    list_display = ("pk", "title", "raiting", "year", "publisher", "genre", "get_tags", "created_at", "image", "user", "count", "price")
    list_display_links = ('title', 'pk')
    search_fields = ('title',)

    def get_tags(self, obj):
        tags = obj.tags.all()
        return "\n".join([t.title for t in tags])


admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Publisher)
admin.site.register(Comment)
admin.site.register(Favorite)
