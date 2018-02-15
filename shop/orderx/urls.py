from django.conf.urls import url
from saleor.core import TOKEN_PATTERN
from saleor.order.urls import urlpatterns

from . import views

urlpatterns[1] = url(r'^%s/payment/$' % (TOKEN_PATTERN,),
        views.payment, name='payment')
