from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    logo = models.ImageField(upload_to="partners/", verbose_name="лого")

    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name = 'партнер'
        verbose_name_plural = 'Партнеры'