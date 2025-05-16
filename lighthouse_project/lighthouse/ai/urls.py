from django.urls import path
from . import views

urlpatterns = [
    path('chatgpt/', views.chatgpt_view, name='chatgpt'),
    path('openchat/', views.openchat_view, name='openchat'),
]