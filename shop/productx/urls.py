from django.conf.urls import url
from saleor.product.urls import urlpatterns
from . import views

urlpatterns += [
    url(r'^onsale/$', views.products_on_sale_index, name='on-sale')
]
