from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import Property

def property_list(request):
    properties = Property.objects.all()  # Будет сортироваться по created_at (как указано в Meta)
    return render(request, 'properties/list.html', {'properties': properties})

def property_detail(request, pk):
    """
    Отображает детальную страницу объекта недвижимости
    """
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'properties/detail.html', {'property': property})

class ServicesView(TemplateView):
    template_name = 'properties/services.html'  # Путь относительно папки templates