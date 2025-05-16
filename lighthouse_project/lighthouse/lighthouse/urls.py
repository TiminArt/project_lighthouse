from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from feedback.views import submit_feedback
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='main.html'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('contacts/', include('contacts.urls')),
    path('accounts/', include('allauth.urls')),

    path('about_us/', TemplateView.as_view(template_name='pages/about_us.html'), name='about_us'),
    path('arenda/', TemplateView.as_view(template_name='pages/arenda.html'), name='arenda'),
    path('ipoteka/', TemplateView.as_view(template_name='pages/ipoteka.html'), name='ipoteka'),
    path('juridic/', TemplateView.as_view(template_name='pages/juridic.html'), name='juridic'),
    path('primary/', TemplateView.as_view(template_name='pages/primary.html'), name='primary'),
    path('support/', TemplateView.as_view(template_name='pages/support.html'), name='support'),
    path('operations/', TemplateView.as_view(template_name='pages/operations.html'), name='operations'),
    path('regional/', TemplateView.as_view(template_name='pages/regional.html'), name='regional'),
    path('commercial/', TemplateView.as_view(template_name='pages/commercial.html'), name='commercial'),
    path('secondary/', TemplateView.as_view(template_name='pages/secondary.html'), name='secondary'),
    path('suburban/', TemplateView.as_view(template_name='pages/suburban.html'), name='suburban'),

    path('submit-feedback/', submit_feedback, name='submit_feedback'),
    path('feedback-success/', TemplateView.as_view(template_name='feedback_success.html'), name='feedback_success'),
    path('properties/', include('properties.urls')),

    path('ai/', include('ai.urls')),
    path('chat/', include('chat.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

