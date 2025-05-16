import openai
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

# Новый клиент OpenAI
openai.api_key = settings.OPENAI_API_KEY
TOGETHER_API_KEY = settings.TOGETHER_API_KEY

# Проверка доступных моделей
# try:
#     models = openai.Model.list()
#     print(models)  # Выведет список доступных моделей в консоль
# except Exception as e:
#     print(f"Error fetching models: {e}")


def chatgpt_view(request):
    messages = []
    if request.method == 'POST':
        user_input = request.POST.get('message')
        messages.append({"role": "user", "content": user_input})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            reply = response['choices'][0]['message']['content']
            messages.append({"role": "assistant", "content": reply})

        except openai.error.RateLimitError:
            # Обработка ошибки, если превышен лимит запросов
            return JsonResponse({'error': 'You have exceeded your API usage quota. Please check your billing details.'})

    return render(request, 'ai/chatgpt.html', {'messages': messages})

def openchat_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('message')
        url = "https://api-inference.huggingface.co/models/Mistral/mistral-7b"  # Укажи правильный URL для модели

        try:
            # Пример POST-запроса с использованием requests
            response = requests.post(
                url,
                json={"input": user_input},
                headers={"Authorization": "Bearer YOUR_API_KEY"}  # Если необходим токен
            )

            if response.status_code == 200:
                model_response = response.json()  # Ответ от модели
                return JsonResponse(model_response)
            else:
                return JsonResponse({'error': 'Failed to get response from the model'})

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)})

    return render(request, 'ai/openchat.html')
    
