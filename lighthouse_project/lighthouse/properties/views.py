from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import Property, PropertyType, City
from .forms import PropertyInquiryForm


@cache_page(60 * 15)  # Кэширование на 15 минут
def property_list(request):
    """
    Отображение списка объектов недвижимости с фильтрацией и пагинацией
    """
    # Параметры фильтрации
    city_id = request.GET.get('city')
    type_id = request.GET.get('type')
    status = request.GET.get('status')

    # Запрос недвижимости
    properties = Property.objects.select_related('property_type', 'agent', 'city')\
                                 .order_by('-is_featured', '-created_at')

    # Применение фильтров
    if city_id:
        properties = properties.filter(city_id=city_id)
    if type_id:
        properties = properties.filter(property_type_id=type_id)
    if status:
        properties = properties.filter(status=status)

    # Пагинация
    paginator = Paginator(properties, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Данные для фильтров
    cities = cache.get_or_set(
        'property_cities',
        list(City.objects.all()),
        60 * 60
    )

    property_types = cache.get('property_types')
    if not property_types:
        property_types = PropertyType.objects.annotate(
            num_properties=Count('properties')
        ).filter(num_properties__gt=0)
        cache.set('property_types', property_types, 60 * 60)

    return render(request, 'properties/list.html', {
        'page_obj': page_obj,
        'cities': cities,
        'property_types': property_types,
        'current_city': city_id,
        'current_type': type_id,
        'current_status': status,
    })


def property_detail(request, pk):
    """
    Детальная страница объекта недвижимости
    """
    property_obj = get_object_or_404(
        Property.objects.select_related('property_type', 'agent', 'city'),
        pk=pk
    )

    # Похожие объекты
    cache_key = f'similar_properties_{pk}'
    similar_properties = cache.get(cache_key)
    if not similar_properties:
        similar_properties = Property.objects.filter(
            property_type=property_obj.property_type,
            city=property_obj.city
        ).exclude(pk=pk).order_by('?')[:3]
        cache.set(cache_key, similar_properties, 60 * 30)

    # Обработка формы
    form = PropertyInquiryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
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

    # Учёт просмотров
    cache_key = f'property_view_{pk}'
    if not cache.get(cache_key):
        property_obj.views += 1
        property_obj.save(update_fields=['views'])
        cache.set(cache_key, True, 60 * 5)

    return render(request, 'properties/detail.html', {
        'property': property_obj,
        'similar_properties': similar_properties,
        'form': form,
    })


class ServicesView(TemplateView):
    template_name = 'properties/services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_properties'] = cache.get_or_set(
            'featured_properties',
            Property.objects.filter(is_featured=True).select_related('property_type', 'city')[:3],
            60 * 30
        )
        return context
