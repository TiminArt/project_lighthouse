from django.urls import path
from . import views 
from .views import ServicesView

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
]