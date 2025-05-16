from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
    path('', TemplateView.as_view(template_name='properties/list.html'), name='properties'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)