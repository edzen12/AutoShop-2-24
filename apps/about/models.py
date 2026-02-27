from django.db import models


class AboutContent(models.Model):
    big_img = models.ImageField(upload_to='about/', verbose_name="Большое фото")
    title = models.CharField(max_length=100)
    desc = models.TextField()
    autograph_img = models.ImageField(upload_to='about/', verbose_name="фото подписи")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'О нас'
        verbose_name = 'о нас'


class PlusAbout(models.Model):
    img = models.ImageField(upload_to='about/', verbose_name="фото")
    title = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Плюсы компании'
        verbose_name = 'плюс компании'


class BlogAbout(models.Model):
    img = models.ImageField(upload_to='about/', verbose_name="фото")
    title = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Блог компании'
        verbose_name = 'блог компании'


class Faq(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Вопросы/Ответы'
        verbose_name = 'вопрос/ответ'


class Testimonials(models.Model):
    avatar = models.ImageField(upload_to='about/', verbose_name="фото")
    name = models.CharField(max_length=150, verbose_name="ФИО")
    position = models.CharField(max_length=100, verbose_name="должность")
    desc = models.TextField()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'отзыв'