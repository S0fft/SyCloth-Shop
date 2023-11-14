from django.views.generic.edit import CreateView

from common.views import TitleMixin
from orders.forms import OrderForm


class OrderCreateView(TitleMixin, CreateView):
    title: str = 'SyCloth - Placing an order'
    template_name: str = 'orders/order-create.html'
    form_class = OrderForm
