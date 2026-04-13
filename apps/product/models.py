from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q, UniqueConstraint

User = get_user_model()


class Category(MPTTModel):
    name = models.CharField(max_length=150, verbose_name="Название категории")
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children',
    )
    is_active = models.BooleanField(default=True, verbose_name="Активация")

    class MPTTMeta:
        order_insertion_by = ['name']

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


class CarModel(models.Model):
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, 
        related_name='models', verbose_name="Бренд"
    )
    name = models.CharField(max_length=100, verbose_name="Модель авто")
    generation = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Поколение"
    )
    year_from = models.PositiveIntegerField(
        verbose_name="Год выпуска", blank=True, null=True
    )

    def __str__(self):
        return f"{self.brand.name} {self.name} {self.generation or ''}"
    
    class Meta:
        verbose_name_plural = 'Модель авто'
        verbose_name = 'модель авто'


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='products'
    )
    car_models = models.ManyToManyField(
        CarModel, related_name='products', verbose_name="Модель авто"
    )
    name = models.CharField(max_length=150, verbose_name="Название товара")
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_main_image(self):
        return self.images.filter(is_main=True).first()

    def get_second_image(self):
        return self.images.filter(is_main=False).first()

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
    
    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(
                product=self.product,
                is_main=True
            ).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Фото товаров'
        verbose_name = 'Фото товара'
        constraints = [
            UniqueConstraint(
                fields=['product'],
                condition=Q(is_main=True),
                name='unique_main_image_per_product'
            )
        ]


class Attribute(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)

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
    
    class Meta:
        verbose_name_plural = 'вариант товара'
        verbose_name = 'Варианты товаров'
        unique_together = ['product', 'sku']


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating}"
    
    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'отзыв'


class Slider(models.Model):
    big_title = models.CharField(verbose_name="Большое название", max_length=100)
    little_title = models.CharField(verbose_name="Мелкие текста", max_length=100)
    img = models.ImageField(upload_to='slider/')
    link = models.CharField(max_length=255, verbose_name="Ссылка")

    def __str__(self):
        return self.big_title
    
    class Meta:
        verbose_name = 'слайдер'
        verbose_name_plural = 'Слайдер'