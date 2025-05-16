# недвижимость
from django.contrib import admin
from .models import Property, PropertyType, PropertyImage
from django.utils.html import format_html


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return ""
    image_preview.short_description = "Превью"


class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'price', 'status', 'floors', 'has_balcony', 'photo_count')
    list_filter = ('status', 'city', 'property_type', 'has_balcony')
    search_fields = ('title', 'address', 'description')
    inlines = [PropertyImageInline]
    readonly_fields = ('photo_previews',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'price', 'status')
        }),
        ('Главное фото', {
            'fields': ('main_photo',)
        }),
        ('Детали', {
            'fields': (
                'bedrooms', 'bathrooms', 'rooms', 'sqft',
                'plot_area', 'floors', 'has_balcony', 
                'address', 'city', 'property_type',
                'agent', 'is_featured'
            )
        }),)

    def photo_count(self, obj):
        return obj.get_all_photos().count()
    photo_count.short_description = 'Фото'

    def photo_previews(self, obj):
        return format_html(
            '<br>'.join(
                f'<img src="{photo.image.url}" style="max-height: 100px; margin: 5px;">' 
                for photo in obj.get_all_photos()
            )
        )
    photo_previews.short_description = 'Превью фото'


admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyType)
