# feedback/admin.py
from django.contrib import admin
from .models import Feedback
from .forms import FeedbackForm  # ← импорт формы

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    form = FeedbackForm  # ← подключение формы

    list_display = ('fullname', 'phone', 'contact_method', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'contact_method')
    search_fields = ('fullname', 'phone', 'email')
    date_hierarchy = 'created_at'
