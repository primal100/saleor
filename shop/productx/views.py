from django.template.response import TemplateResponse
from saleor.product.utils import get_product_list_context
from .filters import NoCategoryProductFilter
from .utils import products_on_sale


class SaleAsCategory(object):
    name = "On Sale"
    slug = "onsale"
    description = "Items on sale now"

    def __str__(self):
        return self.name

def products_on_sale_index(request, *args):
    products = products_on_sale()
    product_filter = NoCategoryProductFilter(
        request.GET, queryset=products)
    ctx = get_product_list_context(request, product_filter)
    return TemplateResponse(request, 'category/index.html', ctx)
