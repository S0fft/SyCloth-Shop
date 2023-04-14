from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)  # Определенная строка, с определенным кол-во символов, уникальное
    description = models.TextField(null=True, blank=True)  # Текстовое поле, безограничения, может быть пустым

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)  # Определенная строка, с определенным кол-во символов
    description = models.TextField()  # Текстовое поле, безограничения
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена, 6 цифр до запятой, 2 цифры после
    quantity = models.PositiveSmallIntegerField(default=0)  # Позитивные малые числа, по умолчанию значение 0
    image = models.ImageField(upload_to="products_images")  # Поле для вставки фотографий, сохроняются в папку "products..."
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"Продукт: {self.name} | Категория: {self.category.name}"
