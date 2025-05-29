from django.db import models
from django.contrib.auth.models import User
from properties.models import Property
from django.utils import timezone

class Client(models.Model):
    full_name = models.CharField("ФИО клиента", max_length=255)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email", blank=True, null=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.phone})"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['-created_at']

class Deal(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="deals", verbose_name="Клиент")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="deals", verbose_name="Объект недвижимости")
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="deals", verbose_name="Агент")
    deal_date = models.DateField("Дата сделки", default=timezone.now)
    price = models.DecimalField("Сумма сделки", max_digits=12, decimal_places=2)
    notes = models.TextField("Примечания", blank=True)

    def __str__(self):
        return f"Сделка: {self.client.full_name} - {self.property.title} ({self.deal_date})"

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"
        ordering = ['-deal_date']

class Report(models.Model):
    title = models.CharField("Название отчёта", max_length=255)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reports", verbose_name="Создано пользователем")
    deals = models.ManyToManyField(Deal, related_name="reports", verbose_name="Сделки в отчёте")
    notes = models.TextField("Описание / примечания", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Отчёт"
        verbose_name_plural = "Отчёты"
        ordering = ['-created_at']
