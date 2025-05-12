# feedback/models.py
from django.db import models
from django.core.exceptions import ValidationError
import re

def validate_phone(value):
    """Проверка формата номера телефона: 89XXXXXXXXX (ровно 11 цифр)"""
    if not re.match(r'^89\d{9}$', value):
        raise ValidationError(
            'Некорректный формат телефона. Используйте формат: 89XXXXXXXXX'
        )

class Feedback(models.Model):
    CONTACT_METHOD_CHOICES = (
        ('call', 'Позвонить'),
        ('email', 'Написать на почту'),
    )

    fullname = models.CharField(
        verbose_name='ФИО',
        max_length=255,
        help_text='Введите полное ФИО'
    )
    
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=11,
        validators=[validate_phone],
        help_text='Формат: 89876543210'
    )
    
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        blank=True,
        help_text='Необязательное поле'
    )
    
    contact_method = models.CharField(
        verbose_name='Способ связи',
        max_length=50,
        choices=CONTACT_METHOD_CHOICES
    )
    
    message = models.TextField(
        verbose_name='Сообщение',
        help_text='Опишите интересующие вас услуги'
    )
    
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    
    is_processed = models.BooleanField(
        verbose_name='Обработано',
        default=False
    )

    def clean(self):
        """Дополнительные проверки перед сохранением"""
        super().clean()
        
        # Очистка и проверка сообщения
        self.message = self.message.strip()
        if len(self.message) < 10:
            raise ValidationError({
                'message': 'Сообщение должно содержать минимум 10 символов'
            })
        
        # Проверка email при выборе способа связи по почте
        if self.contact_method == 'email' and not self.email:
            raise ValidationError({
                'email': 'Укажите email для выбранного способа связи'
            })

    def __str__(self):
        return (
            f"Заявка #{self.id} от {self.fullname} "
            f"({self.created_at.strftime('%d.%m.%Y %H:%M')})"
        )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'is_processed']),
        ]