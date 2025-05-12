from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'phone', 'contact_method', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'contact_method')
    search_fields = ('fullname', 'phone', 'email')
    list_editable = ('is_processed',)
    date_hierarchy = 'created_at'