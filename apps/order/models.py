from django.db import models
from django.contrib.auth import get_user_model
from apps.product.models import ProductVariant

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('processing', 'Процесс'),
        ('completed', 'Выполнено'),
        ('canceled', 'Отменено'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заказ {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.variant.name


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, 
        related_name='shipping', verbose_name="адрес доставки"
    )
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    city = models.CharField(max_length=150)
    address = models.TextField()

    def __str__(self):
        return self.full_name


class Payment(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, 
        related_name='payment', verbose_name="Заказ"
    )
    method = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.method