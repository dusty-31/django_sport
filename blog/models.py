from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва категорії')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL slug')
    description = models.TextField(blank=True, verbose_name='Опис категорії')
    icon = models.CharField(max_length=50, default='fas fa-folder', verbose_name='Іконка')
    color = models.CharField(max_length=20, default='primary', verbose_name='Колір')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:blog_category', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Назва тегу')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL slug')
    color = models.CharField(max_length=20, default='gray', verbose_name='Колір')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:blog_tag', kwargs={'slug': self.slug})


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Чернетка'),
        ('published', 'Опубліковано'),
        ('archived', 'Архів'),
    ]

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL slug')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name='Категорія')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги')

    excerpt = models.TextField(max_length=300, verbose_name='Короткий опис')
    content = models.TextField(verbose_name='Контент')

    featured_image = models.URLField(blank=True, verbose_name='Головне зображення')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендована стаття')

    views_count = models.PositiveIntegerField(default=0, verbose_name='Кількість переглядів')
    reading_time = models.PositiveIntegerField(default=5, verbose_name='Час читання (хв)')

    meta_description = models.CharField(max_length=160, blank=True, verbose_name='Meta опис')
    meta_keywords = models.CharField(max_length=255, blank=True, verbose_name='Meta ключові слова')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата публікації')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:blog_post', kwargs={'slug': self.slug})

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.TextField(verbose_name='Коментар')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='Батьківський коментар')

    is_approved = models.BooleanField(default=True, verbose_name='Схвалено')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        ordering = ['created_at']

    def __str__(self):
        return f'Коментар від {self.author.username} до "{self.post.title}"'