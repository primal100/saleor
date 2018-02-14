from django.conf.urls import url
from saleor.core.urls import urlpatterns
from . import views

urlpatterns += [
    url(r'^currency-change/', views.changecurrency, name='currencychange'),
]
