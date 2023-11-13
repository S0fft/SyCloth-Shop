from django.views.generic.edit import CreateView

from common.views import TitleMixin
from orders.forms import OrderForm


class OrderCreateView(TitleMixin, CreateView):
    title = 'SyCloth - Placing an order'
    template_name = 'orders/order-create.html'
    form_class = OrderForm
