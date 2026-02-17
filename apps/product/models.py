from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название категории")
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children',
    )
    is_active = models.BooleanField(default=True, verbose_name="Активация")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'категория'


class Brand(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название бренда")
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='brand/', verbose_name="Лого бренда")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Бренд'
        verbose_name = 'бренд'


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL,
        related_name='products', blank=True, null=True
    )
    name = models.CharField(max_length=150, verbose_name="Название товара")
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'товар'
    

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(verbose_name="Фото", upload_to='product')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name_plural = 'Фото товаров'
        verbose_name = 'Фото товара'


class Attribute(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100)

    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name_plural = 'Атрибуты'
        verbose_name = 'атрибут'


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE,
        related_name='values'
    )
    value = models.CharField(verbose_name="Название", max_length=100)

    def __str__(self):
        return f"{self.attribute.name} {self.value}"
    
    class Meta:
        verbose_name_plural = 'Значения атрибутов'
        verbose_name = 'значения атрибута'


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, 
        related_name='variants', verbose_name="Товар"
    )
    attributes = models.ManyToManyField(AttributeValue, verbose_name="Атрибуты товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество товара на складе")
    sku = models.CharField(max_length=100, unique=True, verbose_name="Артикул товара")

    def __str__(self):
        return f"{self.product.name} {self.sku}"


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating}"
    
    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'отзыв'