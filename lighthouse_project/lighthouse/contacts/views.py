from django.shortcuts import render, redirect
from django.contrib import messages

def contact_form(request):
    if request.method == 'POST':
        # Обработка формы
        messages.success(request, 'Сообщение отправлено!')
        return redirect('contact_success')
    return render(request, 'contacts/contact.html')

def contact_success(request):
    return render(request, 'contacts/success.html')