from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name: str = 'products/index.html'
    title: str = 'SyCloth'

    def get_context_data(self) -> dict[str, any]:
        context = super().get_context_data()
        context['is_prom']: bool = True

        return context


class ProductsListView(TitleMixin, ListView):
    title: str = 'SyCloth - Catalog'
    model = Product
    template_name: str = 'products/products.html'
    context_object_name: str = 'products'
    paginate_by: int = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id: int = self.kwargs.get('category_id')

        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self) -> dict[str, any]:
        context = super().get_context_data()
        categories = cache.get('categories')

        if not categories:
            context['categories']: str = ProductCategory.objects.all()
            cache.set('categories', context['categories'], 30)
        else:
            context['categories']: str = ProductCategory.objects.all()

        return context


@login_required
def basket_add(request, product_id: int):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id: int):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
