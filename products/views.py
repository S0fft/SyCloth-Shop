# Файл для отображения шаблонов (контента) на сайте
# Функции = контроллеры = обработчики запросов = виьюхи

from django.shortcuts import render

# Create your views here.


def index(request):
    context = {
        "title": "Test Title",
        "username": "valery",
    }
    return render(request, "products/index.html")


def products(request):
    return render(request, "products/products.html")
