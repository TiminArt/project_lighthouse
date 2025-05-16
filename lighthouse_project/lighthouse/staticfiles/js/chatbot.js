// Функция для отправки сообщения
        $('#chat-form').on('submit', function(event) {
            event.preventDefault();
            const userInput = $('#user-input').val();
            if (userInput.trim()) {
                $('#chat-box').append('<p><strong>Вы:</strong> ' + userInput + '</p>');
                $('#user-input').val('');

                $.ajax({
                    url: '/chat/', 
                    type: 'POST',
                    data: {
                        'question': userInput,
                        'csrfmiddlewaretoken': '{{ csrf_token }}'
                    },
                    success: function(response) {
                        $('#chat-box').append('<p><strong>Ответ:</strong> ' + response.answer + '</p>');
                        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
                    },
                    error: function() {
                        $('#chat-box').append('<p><strong>Ответ:</strong> Ошибка, попробуйте снова.</p>');
                    }
                });
            }
        });