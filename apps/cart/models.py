from django.db import models 
from django.conf import settings
from apps.product.models import Product

User = settings.AUTH_USER_MODEL

class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True, blank=True, related_name='carts'
    )
    session_key = models.CharField(max_length=60, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина {self.id}'
    
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())
    
    class Meta:
        verbose_name='корзина'
        verbose_name='Корзина'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,on_delete=models.CASCADE, 
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} {self.quantity}"

    def total_price(self):
        return self.price * self.quantity
    
    class Meta:
        unique_together = ('cart', 'product')
