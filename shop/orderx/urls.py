from django.conf.urls import url
from saleor.core import TOKEN_PATTERN
from saleor.order.urls import urlpatterns
from . import views

urlpatterns += [
    url(r'^%s/create-payment/(?P<variant>[-\w]+)/$' % (TOKEN_PATTERN,),
        views.create_payment, name='create-payment'),
]
