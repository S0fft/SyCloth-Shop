from django.urls import include, path
from rest_framework import routers

from api.views import ProductModelViewSet

app_name: str = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
