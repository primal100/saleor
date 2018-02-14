from saleor.product.filters import ProductFilter
from saleor.product.models import ProductAttribute

class NoCategoryProductFilter(ProductFilter):

    def _get_attributes(self):
        product_attributes = (
            ProductAttribute.objects.all()
            .prefetch_related('values')
            .distinct())
        variant_attributes = (
            ProductAttribute.objects.all()
            .prefetch_related('values')
            .distinct())
        return product_attributes, variant_attributes
