from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    category: str = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Product
        fields: list[str] = ['id', 'name', 'description', 'price', 'quantity', 'image', 'category']
