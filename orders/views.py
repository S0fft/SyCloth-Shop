from http import HTTPStatus
from typing import Any

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from base import settings
from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name: str = 'orders/success.html'
    title: str = 'Thank you for your order!'


class CanceledTemplateView(TemplateView):
    template_name: str = 'orders/canceled.html'


class OrderListView(TitleMixin, ListView):
    title: str = 'SyCloth - Orders'
    template_name: str = 'orders/orders.html'
    context_object_name: str = 'orders'
    queryset: list = Order.objects.all()
    ordering: str = ('created')

    def get_queryset(self) -> list[str]:
        queryset = super().get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name: str = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = f'SyCloth - Order № {self.object.id}'

        return context


class OrderCreateView(TitleMixin, CreateView):
    title: str = 'SyCloth - Placing an order'
    template_name: str = 'orders/order-create.html'
    form_class = OrderForm
    success_url: str = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        super().post(request, *args, **kwargs)

        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user

        return super().form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        fulfill_order(session)

    return HttpResponse(status=200)


def fulfill_order(session):
    order_id: int = int(session.metadata.order_id)

    order: int = Order.objects.get(id=order_id)
    order.update_after_payment()
