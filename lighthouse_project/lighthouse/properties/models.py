from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PropertyType(models.Model):
    """Модель типа недвижимости"""
    name = models.CharField(max_length=100, verbose_name="Название типа")

    class Meta:
        verbose_name = "Тип недвижимости"
        verbose_name_plural = "Типы недвижимости"
        ordering = ['name']

    def __str__(self):
        return self.name

class Property(models.Model):
    """Модель объекта недвижимости"""
    PROPERTY_STATUS_CHOICES = [
        ('sale', 'На продажу'),
        ('rent', 'Аренда'),
    ]

    # Основные поля
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")
    bedrooms = models.PositiveIntegerField(verbose_name="Количество спален")
    bathrooms = models.PositiveIntegerField(verbose_name="Количество ванных")
    sqft = models.PositiveIntegerField(verbose_name="Площадь (кв. футы)")

    # Адресные данные
    address = models.CharField(max_length=255, verbose_name="Адрес")
    city = models.CharField(max_length=100, verbose_name="Город")

    # Связи и статусы
    status = models.CharField(
        max_length=10,
        choices=PROPERTY_STATUS_CHOICES,
        default='sale',
        verbose_name="Статус"
    )
    property_type = models.ForeignKey(
        PropertyType,
        on_delete=models.PROTECT,
        related_name='properties',
        verbose_name="Тип объекта"
    )
    agent = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='properties',
        verbose_name="Агент"
    )

    # Изображения
    main_photo = models.ImageField(upload_to='properties/')
    photo_1 = models.ImageField(upload_to='properties/', blank=True, null=True)
    photo_2 = models.ImageField(upload_to='properties/', blank=True, null=True)
    photo_3 = models.ImageField(upload_to='properties/', blank=True, null=True)

    # Флаги и даты
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Объект недвижимости"
        verbose_name_plural = "Объекты недвижимости"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['price']),
            models.Index(fields=['city']),
        ]

    def __str__(self):
        return f"{self.title} - {self.city}"