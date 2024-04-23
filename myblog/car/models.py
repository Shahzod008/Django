from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Car(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    slug = models.SlugField(max_length=20, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True , verbose_name='Текст статьи')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name='Фото' )
    time_create = models.DateTimeField(auto_now_add=True , verbose_name='Время оздания')
    time_update = models.DateTimeField(auto_now=True , verbose_name='Время изминения')
    is_published = models.BooleanField(default=True , verbose_name='Публикация')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    
    class Meta:
        verbose_name = 'записи'
        verbose_name_plural = 'записи'
        ordering = ['id']
        ordering = ['-time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категории")
    slug = models.SlugField(max_length=300, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
    
    class Meta:
        verbose_name = 'категории'
        verbose_name_plural = 'Категории'
        ordering = ['id']

class ContactMessage(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'заявки'
        verbose_name_plural = 'Заявки'
        ordering = ['id']

    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From {self.sender.username} at {self.timestamp}'