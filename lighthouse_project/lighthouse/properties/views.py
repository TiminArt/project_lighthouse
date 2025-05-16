from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import Property, PropertyType
from .forms import PropertyInquiryForm

@cache_page(60 * 15)  # Кэширование на 15 минут
def property_list(request):
    """
    Отображение списка объектов недвижимости с фильтрацией и пагинацией
    """
    # Получаем параметры фильтрации из GET-запроса
    city = request.GET.get('city')
    type_id = request.GET.get('type')
    status = request.GET.get('status')
    
    # Базовый запрос с оптимизацией (select_related для ForeignKey)
    properties = Property.objects.select_related('property_type', 'agent')\
                                .order_by('-is_featured', '-created_at')
    
    # Применяем фильтры, если они есть
    if city:
        properties = properties.filter(city__iexact=city)
    if type_id:
        properties = properties.filter(property_type_id=type_id)
    if status:
        properties = properties.filter(status=status)
    
    # Пагинация - 6 объектов на странице
    paginator = Paginator(properties, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Получаем данные для фильтров (города и типы недвижимости)
    cities = cache.get('property_cities')
    if not cities:
        cities = Property.objects.values_list('city', flat=True).distinct()
        cache.set('property_cities', cities, 60 * 60)  # Кэшируем на 1 час
    
    property_types = cache.get('property_types')
    if not property_types:
        property_types = PropertyType.objects.annotate(
            num_properties=Count('properties')
        ).filter(num_properties__gt=0)
        cache.set('property_types', property_types, 60 * 60)  # Кэшируем на 1 час
    
    return render(request, 'properties/list.html', {
        'page_obj': page_obj,        # Объекты для текущей страницы
        'cities': cities,            # Все города для фильтра
        'property_types': property_types,  # Все типы недвижимости
        'current_city': city,        # Текущий выбранный город
        'current_type': type_id,     # Текущий выбранный тип
        'current_status': status,    # Текущий выбранный статус
    })

def property_detail(request, pk):
    """
    Детальная страница объекта недвижимости
    """
    # Получаем объект или 404, с оптимизацией запросов
    property_obj = get_object_or_404(
        Property.objects.select_related('property_type', 'agent'),
        pk=pk
    )
    
    # Получаем похожие объекты (из кэша или БД)
    cache_key = f'similar_properties_{pk}'
    similar_properties = cache.get(cache_key)
    
    if not similar_properties:
        similar_properties = Property.objects.filter(
            property_type=property_obj.property_type,
            city=property_obj.city
        ).exclude(pk=pk).order_by('?')[:3]  # 3 случайных объекта
        cache.set(cache_key, similar_properties, 60 * 30)  # Кэшируем на 30 минут
    
    # Обработка формы запроса информации
    form = PropertyInquiryForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        # Отправка email с запросом
        send_mail(
            subject=f'Запрос по объекту: {property_obj.title}',
            message=f"""
                Сообщение от: {form.cleaned_data['name']}
                Email: {form.cleaned_data['email']}
                Телефон: {form.cleaned_data['phone']}
                Сообщение: {form.cleaned_data['message']}

                Объект: {property_obj.title} ({request.build_absolute_uri(property_obj.get_absolute_url())})
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[property_obj.agent.email, settings.SALES_EMAIL],
            fail_silently=False,
        )
        return redirect('property_detail', pk=pk)
    
    # Увеличение счетчика просмотров (с кэшированием)
    cache_key = f'property_view_{pk}'
    if not cache.get(cache_key):
        property_obj.views += 1
        property_obj.save(update_fields=['views'])
        cache.set(cache_key, True, 60 * 5)  # Учитываем просмотр раз в 5 минут
    
    return render(request, 'properties/detail.html', {
        'property': property_obj,
        'similar_properties': similar_properties,
        'form': form,
    })

class ServicesView(TemplateView):
    # Представление для страницы услуг
    template_name = 'properties/services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем рекомендуемые объекты из кэша или БД
        context['featured_properties'] = cache.get_or_set(
            'featured_properties',
            Property.objects.filter(is_featured=True).select_related('property_type')[:3],
            60 * 30  # Кэшируем на 30 минут
        )
        return context