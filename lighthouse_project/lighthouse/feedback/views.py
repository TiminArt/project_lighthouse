from django.shortcuts import redirect
from django.urls import reverse
from .models import Feedback
import re
from django.core.exceptions import ValidationError

def submit_feedback(request):
    if request.method == 'POST':
        Feedback.objects.create(
            fullname=request.POST['fullname'],
            phone=request.POST['phone'],
            email=request.POST.get('email', ''),
            contact_method=request.POST['contact_method'],
            message=request.POST['message']
        )
        return redirect(reverse('feedback_success'))
    return redirect('/')


def validate_phone(value):
    pattern = r'^\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}$'
    if not re.match(pattern, value):
        raise ValidationError('Некорректный формат телефона')