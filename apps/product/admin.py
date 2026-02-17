from django.contrib import admin
from apps.product.models import *


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(Review) 