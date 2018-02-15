from django.conf.urls import include, url
from saleor.urls import urlpatterns
from shop.corex.urls import urlpatterns as corex_urls
from shop.orderx.urls import urlpatterns as orderx_urls
from shop.productx.urls import urlpatterns as productx_urls

urlpatterns[0] = url(r'^', include(corex_urls))
urlpatterns[6] = url(r'^order/', include((orderx_urls, 'order'), namespace='order'))
urlpatterns[7] = url(r'^products/',
        include((productx_urls, 'product'), namespace='product'))
