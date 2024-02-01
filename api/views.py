from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from products.models import Product
from products.serializers import ProductSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()
