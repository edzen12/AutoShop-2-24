from django.db import models

class ContactPage(models.Model):
    map = models.TextField(verbose_name='карта')
    title = models.CharField(max_length=100)
    desc = models.TextField()
    address = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Контакты'
        verbose_name = 'контакт'

class ContactRequest(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.email}"
    
    class Meta:
        verbose_name_plural = 'Заявки на сайте'
        verbose_name = 'заявка на сайте'

