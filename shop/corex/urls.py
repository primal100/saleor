from django.conf.urls import url
from django.views.generic import TemplateView
from saleor.core.urls import urlpatterns
from . import views

urlpatterns += [
    url('contact/', views.ContactView.as_view(template_name="contact.html"), name='contact-us'),
    url(r'^currency-change/', views.changecurrency, name='currencychange'),
    url(r'^privacy-policy/', TemplateView.as_view(template_name='privacypolicy.html'), name="privacy-policy"),
    url(r'^refund-policy/', TemplateView.as_view(template_name='refundpolicy.html'), name="refund-policy"),
    url(r'^terms/', TemplateView.as_view(template_name='termsandconditions.html'), name="terms")
]
