def products_on_sale():
    from saleor.product.models import Product
    product_ids = Product.sale_set.through.objects.values_list('product', flat=True).distinct()
    return Product.objects.filter(id__in=product_ids).order_by('price')
