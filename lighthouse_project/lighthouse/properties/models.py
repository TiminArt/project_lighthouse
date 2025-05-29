from django.db import models 
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


class PropertyType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название типа")
    icon = models.CharField(max_length=50, blank=True, help_text="Иконка Font Awesome")

    class Meta:
        verbose_name = "Тип недвижимости"
        verbose_name_plural = "Типы недвижимости"
        ordering = ['name']

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название города", unique=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ['name']

    def __str__(self):
        return self.name


class Property(models.Model):
    PROPERTY_STATUS_CHOICES = [
        ('sale', 'На продажу'),
        ('rent', 'Аренда'),
    ]
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Описание")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")
    rooms = models.PositiveIntegerField(verbose_name="Количество комнат")
    bedrooms = models.PositiveIntegerField(verbose_name="Количество спален")
    bathrooms = models.PositiveIntegerField(verbose_name="Количество ванных")
    sqft = models.PositiveIntegerField(verbose_name="Площадь (кв. м)")
    plot_area = models.PositiveIntegerField(verbose_name="Площадь участка (соток)", blank=True, null=True)
    views = models.PositiveIntegerField(default=0, editable=False)
    floor_number = models.PositiveIntegerField(verbose_name="Этаж", default=1)
    floors = models.PositiveIntegerField(verbose_name="Количество этажей в доме")
    has_balcony = models.BooleanField(default=False, verbose_name="Балкон")
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="properties", verbose_name="Город")
    status = models.CharField(max_length=10, choices=PROPERTY_STATUS_CHOICES, default='sale', verbose_name="Статус")
    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT, related_name='properties', verbose_name="Тип объекта")
    agent = models.ForeignKey(User, on_delete=models.PROTECT, related_name='properties', verbose_name="Агент")
    main_photo = models.ImageField(upload_to='properties/', verbose_name="Главное фото")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Объект недвижимости"
        verbose_name_plural = "Объекты недвижимости"
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['price']),
            models.Index(fields=['city']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.title} - {self.city}"

    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.title}-{self.city}")
            slug = base_slug
            counter = 1
            while Property.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_all_photos(self):
        return self.images.all()


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images', verbose_name="Объект недвижимости")
    image = models.ImageField(upload_to='properties/gallery/', verbose_name="Фото")

    class Meta:
        verbose_name = "Доп. фото"
        verbose_name_plural = "Доп. фотографии"

    def __str__(self):
        return f"Фото для {self.property.title}"
