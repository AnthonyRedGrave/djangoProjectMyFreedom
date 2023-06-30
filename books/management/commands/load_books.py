from django.core.management.base import BaseCommand
import requests
import random
from books.models import Publisher, Book
import django

class Command(BaseCommand):
    help = 'Загрузка книг из другого источника'

    def handle(self, *args, **options):
        print("команда запустилась")
        url = "http://gen.lib.rus.ec/json.php?fields=Title,Author,Year,publisher&ids=1,2,3,4,5,6,7"
        response = requests.get(url)

        languages = ["ru", "en", "fr"]



        for book in response.json():
            # print()
            # print(book['author'])
            # print(book['year'])
            # print(book['publisher'])
            language = random.choice(languages)

            if not Publisher.objects.filter(title = book['publisher']).last():
                publisher = Publisher.objects.create(title = book['publisher'],
                                         language = language)
            else:
                publisher = Publisher.objects.filter(title = book['publisher']).last()


            # новым книгам давать рандомный рейтинг от 0 до 10

            try:
                if not Book.objects.filter(title=book['title']).last():
                    Book.objects.create(title = book['title'],
                                        author = book['author'],
                                        year = book['year'],
                                        publisher = publisher)
            except django.db.utils.IntegrityError:
                Book.objects.create(title=book['title'],
                                    author=book['author'],
                                    year=book['year'])
