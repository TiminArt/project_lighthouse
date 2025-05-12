from django.contrib import admin
from .models import Property, PropertyType

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'city', 'status')
    list_filter = ('status', 'property_type')

admin.site.register(PropertyType)