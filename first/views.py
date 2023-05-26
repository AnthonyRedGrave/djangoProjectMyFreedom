from django.http import HttpResponse

def first(request):
    return HttpResponse("<h1>Здесь будут сайт с книгами!</h1>")


def second_func(request):
    return HttpResponse("<h1>Олег</h1>")