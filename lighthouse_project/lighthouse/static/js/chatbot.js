$('#chat-form').on('submit', function(event) {
    event.preventDefault();
    const userInput = $('#user-input').val();
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    if (userInput.trim()) {
        $('#chat-box').append('<p><strong>Вы:</strong> ' + userInput + '</p>');
        $('#user-input').val('');

        $.ajax({
            url: '/chat/',
            type: 'POST',
            data: {
                'question': userInput,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                $('#chat-box').append('<p><strong>Ответ:</strong> ' + response.answer + '</p>');
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
            },
            error: function(xhr) {
                $('#chat-box').append('<p><strong>Ответ:</strong> Ошибка ' + xhr.status + ', попробуйте снова.</p>');
            }
        });
    }
});
