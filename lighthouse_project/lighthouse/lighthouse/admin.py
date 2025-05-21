from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'phone')



# admin.site.site_header = "Маяк - Администрирование"
# admin.site.site_title = "Админ-панель Маяк"
# admin.site.index_title = "Управление сайтом"