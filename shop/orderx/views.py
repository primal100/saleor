from saleor.core.utils import get_client_ip
from saleor.order.forms import PaymentDeleteForm, PaymentMethodsForm
from saleor.order.models import Order, Payment
from saleor.order.utils import check_order_status

from .forms import ModalPaymentForm

from django.conf import settings
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import pgettext_lazy
from payments import PaymentStatus
from payments.core import provider_factory


def payment(request, token):
    orders = Order.objects.prefetch_related('groups__lines__product')
    orders = orders.select_related('billing_address', 'shipping_address',
                                   'user')
    order = get_object_or_404(orders, token=token)
    groups = order.groups.all()
    payments = order.payments.all()
    form_data = request.POST or None
    try:
        waiting_payment = order.payments.get(status=PaymentStatus.WAITING)
    except Payment.DoesNotExist:
        waiting_payment = None
        waiting_payment_form = None
    else:
        form_data = None
        waiting_payment_form = PaymentDeleteForm(
            None, order=order, initial={'payment_id': waiting_payment.id})
    if order.is_fully_paid():
        form_data = None
    payment_form = None
    if not order.is_pre_authorized():
        payment_form = PaymentMethodsForm(form_data)
        # FIXME: redirect if there is only one payment method
        if payment_form.is_valid():
            payment_method = payment_form.cleaned_data['method']
            return redirect('order:payment', token=order.token,
                            variant=payment_method)
    stripe_provider = provider_factory("stripe")
    stripe_payment = create_payment(request, variant="stripe", token=token)
    stripe_form = ModalPaymentForm(email=order.user_email, provider=stripe_provider, payment=stripe_payment)
    return TemplateResponse(request, 'order/payment.html',
                            {'order': order, 'groups': groups,
                             'payment_form': payment_form,
                             'waiting_payment': waiting_payment,
                             'waiting_payment_form': waiting_payment_form,
                             'payments': payments,
                             'stripe_form': stripe_form})

@check_order_status
def create_payment(request, order, variant):
    billing = order.billing_address
    total = order.total
    defaults = {'total': total.gross,
                'tax': total.tax, 'currency': total.currency,
                'delivery': order.shipping_price.gross,
                'billing_first_name': billing.first_name,
                'billing_last_name': billing.last_name,
                'billing_address_1': billing.street_address_1,
                'billing_address_2': billing.street_address_2,
                'billing_city': billing.city,
                'billing_postcode': billing.postal_code,
                'billing_country_code': billing.country.code,
                'billing_email': order.user_email,
                'description': pgettext_lazy(
                    'Payment description', 'Order %(order_number)s') % {
                        'order_number': order},
                'billing_country_area': billing.country_area,
                'customer_ip_address': get_client_ip(request)}
    variant_choices = settings.CHECKOUT_PAYMENT_CHOICES
    if variant not in [code for code, dummy_name in variant_choices]:
        raise Http404('%r is not a valid payment variant' % (variant,))
    with transaction.atomic():
        payment, dummy_created = Payment.objects.get_or_create(
            variant=variant, status=PaymentStatus.WAITING, order=order,
                defaults=defaults)
        payment.status = PaymentStatus.INPUT
        payment.save()
        return payment
