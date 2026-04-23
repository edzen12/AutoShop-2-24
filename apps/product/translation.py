from modeltranslation.translator import register, TranslationOptions
from apps.product.models import Product, Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['name']


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ['name', 'description']