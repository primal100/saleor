from django.conf.urls import url
from saleor.core.urls import urlpatterns
from . import views

urlpatterns += [
    url('contact/', views.ContactView.as_view(template_name="contact.html"), name='contact-us'),
    url(r'^currency-change/', views.changecurrency, name='currencychange'),
]
