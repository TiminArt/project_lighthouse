import openai
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

# Ключи из settings
openai.api_key = settings.OPENAI_API_KEY
TOGETHER_API_KEY = settings.TOGETHER_API_KEY


def translate_text(text: str, target_lang='ru') -> str:
    """
    Переводит текст на target_lang с помощью публичного Google Translate API.
    """
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": target_lang,
        "dt": "t",
        "q": text,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        translation = response.json()[0][0][0]
        return translation
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return text  # возвращаем исходный текст, если перевод не удался


def chatgpt_view(request):
    messages = []
    if request.method == 'POST':
        if 'clear_chat' in request.POST:
            # Очистка истории сообщений
            messages = []
        else:
            user_input = request.POST.get('message')
            if user_input:
                messages.append({"role": "user", "content": user_input})

                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages
                    )
                    reply = response['choices'][0]['message']['content']
                    # Переводим ответ на русский
                    translated_reply = translate_text(reply, target_lang='ru')

                    messages.append({"role": "assistant", "content": translated_reply})

                except openai.error.RateLimitError:
                    return JsonResponse({'error': 'You have exceeded your API usage quota. Please check your billing details.'})

    return render(request, 'ai/chatgpt.html', {'messages': messages})


def openchat_view(request):
    # Получаем список сообщений из сессии, или создаём пустой
    messages = request.session.get('chat_messages', [])

    if request.method == 'POST':
        if 'clear_chat' in request.POST:
            # Очистка сессионной истории
            messages = []
            request.session['chat_messages'] = messages
        else:
            user_input = request.POST.get('message')
            if user_input:
                messages.append({"role": "user", "content": user_input})

                url = "https://api.together.xyz/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {TOGETHER_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "mistralai/Mistral-7B-Instruct-v0.1",
                    "messages": messages,
                    "temperature": 0.7
                }

                try:
                    response = requests.post(url, headers=headers, json=payload)
                    if response.status_code == 200:
                        result = response.json()
                        reply = result['choices'][0]['message']['content']

                        # Переводим ответ ассистента
                        translated_reply = translate_text(reply, target_lang='ru')

                        # Добавляем ответ ассистента в историю
                        messages.append({"role": "assistant", "content": translated_reply})

                        # Сохраняем обновлённую историю в сессию
                        request.session['chat_messages'] = messages

                    else:
                        messages.append({"role": "assistant", "content": f"Ошибка API: {response.status_code}"})
                        request.session['chat_messages'] = messages

                except requests.exceptions.RequestException as e:
                    messages.append({"role": "assistant", "content": f"Ошибка запроса: {str(e)}"})
                    request.session['chat_messages'] = messages

    return render(request, 'ai/openchat.html', {'messages': messages})
