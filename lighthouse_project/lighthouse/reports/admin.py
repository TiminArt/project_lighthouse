from django.contrib import admin
from django import forms
from .models import Client, Deal, Report

class DealAdminForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = '__all__'
        widgets = {
            'deal_date': forms.DateInput(attrs={'type': 'date'}),
        }

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'created_at')
    search_fields = ('full_name', 'phone', 'email')
    ordering = ('-created_at',)

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    form = DealAdminForm  
    list_display = ('client', 'property', 'agent', 'deal_date', 'price')
    search_fields = ('client__full_name', 'property__title', 'agent__username')
    list_filter = ('deal_date', 'agent')
    ordering = ('-deal_date',)
    autocomplete_fields = ['client', 'property', 'agent']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'notes', 'created_by__username')
    list_filter = ('created_at',)
    filter_horizontal = ('deals',)
    ordering = ('-created_at',)
