from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name 
    
    def get_absolute_url(self):
        return reverse("posts_by_tag", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'Теги'
        verbose_name = 'тег'


class Post(models.Model):
    tags = models.ManyToManyField(Tag, related_name='posts', verbose_name="Теги")
    title = models.CharField(max_length=100, verbose_name="Название")
    img = models.ImageField(upload_to='posts/', verbose_name="Фото")
    slug = models.SlugField(unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Посты'
        verbose_name = 'пост'