from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'  

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError('Сообщение должно содержать минимум 10 символов')
        return message

    def clean(self):
        cleaned_data = super().clean()
        contact_method = cleaned_data.get('contact_method')
        email = cleaned_data.get('email')

        if contact_method == 'email' and not email:
            self.add_error('email', 'Укажите email для выбранного способа связи')
            
