from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    contact_method = forms.ChoiceField(
        label='Как связаться?',
        choices=Application.CONTACT_METHODS,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Application
        fields = [
            'full_name', 
            'phone_number', 
            'email', 
            'contact_method', 
            'services_description'
        ]
        labels = {
            'full_name': 'ФИО*',
            'phone_number': 'Номер телефона*',
            'email': 'Email (необязательно)',
            'services_description': 'Опишите, какие услуги вас интересуют*'
        }