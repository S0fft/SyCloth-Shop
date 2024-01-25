from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from base import settings
from common.views import TitleMixin
from orders.forms import OrderForm
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name: str = 'orders/success.html'
    title: str = 'Thank you for your order!'


class CanceledTemplateView(TemplateView):
    template_name: str = 'orders/canceled.html'


class OrderCreateView(TitleMixin, CreateView):
    title: str = 'SyCloth - Placing an order'
    template_name: str = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')

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
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

    line_items = session.line_items
    fulfill_order(line_items)

    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)

    print("Fulfilling order")
