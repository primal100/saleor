from django.conf import settings
from django.db import transaction
from django.http import Http404
from django.utils.translation import pgettext_lazy
from payments import PaymentStatus

from saleor.core.utils import get_client_ip
from saleor.order.models import Payment
from saleor.order.utils import check_order_status

@check_order_status
def create_payment(request, order, variant):
    billing = order.billing_address
    total = order.get_total()
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
