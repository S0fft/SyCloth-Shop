from rest_framework import fields, serializers

from products.models import Basket, Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    category: str = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields: list[str] = ['id', 'name', 'description', 'price', 'quantity', 'image', 'category']


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sum: int = fields.FloatField(required=False)
    total_sum: int = fields.SerializerMethodField()
    total_quantity: int = fields.SerializerMethodField()

    class Meta:
        model = Basket
        fields: list[str] = ['id', 'product', 'quantity', 'sum', 'total_sum', 'total_quantity', 'created_timestamp']
        read_only_fields: list[str] = ['created_timestamp']

    def get_total_sum(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_sum()

    def get_total_quantity(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_quantity()
