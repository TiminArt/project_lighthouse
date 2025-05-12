from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect

# Функция для регистрации
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Замените 'home' на ваш URL
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

# Функция для профиля
def profile(request):
    return render(request, 'accounts/profile.html')