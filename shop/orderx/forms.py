from django import forms
from payments.stripe.forms import StripeFormMixin, BasePaymentForm, StripeCheckoutWidget, RedirectNeeded
from payments import PaymentStatus

class ModalPaymentForm(StripeFormMixin, BasePaymentForm):

    def __init__(self, *args, email=None, **kwargs):
        super(StripeFormMixin, self).__init__(hidden_inputs=False, *args, **kwargs)
        attrs = {'email': email}
        widget = StripeCheckoutWidget(provider=self.provider, payment=self.payment, attrs=attrs)
        self.fields['stripeToken'] = forms.CharField(widget=widget)
        if self.is_bound and not self.data.get('stripeToken'):
            self.payment.change_status(PaymentStatus.REJECTED)
            raise RedirectNeeded(self.payment.get_failure_url())
