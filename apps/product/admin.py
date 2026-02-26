from django.contrib import admin
from apps.product.models import *
from mptt.admin import DraggableMPTTAdmin
from django.utils.html import format_html

admin.site.register(Slider)

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'something', 'is_active')
    list_display_links=('something',)
    list_filter = ('is_active',)
    search_fields = ('name',)
    mptt_level_indent = 20
    prepopulated_fields = {'slug': ('name',)}

    def something(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.name, 
        )
    something.short_description = ('Все категории')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',) 
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    show_change_link = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'brand', 'price', 'stock', 
        'is_available', 'created_at'
    )
    list_filter = ('is_available', 'category')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline]

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute','value')
    list_filter = ('attribute',)
    search_fields = ('value',)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product','price', 'stock', 'sku')
    list_filter = ('product',)
    search_fields = ('sku',)
    filter_horizontal = ('attributes',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product','user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('product__name','user__username') 

